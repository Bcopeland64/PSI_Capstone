"""
data_handler.py
----------------
All external I/O lives here: reading connection-log CSVs, reading the JSON
watchlist config, writing reports back out as JSON/CSV, and persisting a
history of past runs in a small SQLite database.

Separating this from logic.py means the analysis functions can be unit
tested with in-memory data, with no disk or database involved.
"""

import csv
import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from typing import Iterator, List

from src.models import Connection, TriageReport

DEFAULT_DB_PATH = os.path.join("data", "triage_history.db")


# ---------------------------------------------------------------------------
# CSV / JSON input
# ---------------------------------------------------------------------------

def load_connections(csv_path: str) -> List[Connection]:
    """Read a connection-log CSV into a list of validated Connection objects.

    Rows that fail validation are skipped with a note printed to stderr-style
    output by the caller (logic.py), rather than crashing the whole run --
    a single malformed log line shouldn't abort a triage.
    """
    connections = []
    skipped = 0
    with open(csv_path, newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                connections.append(Connection.from_row(row))
            except ValueError:
                skipped += 1
    return connections, skipped


def load_watchlist(json_path: str) -> dict:
    """Load the watchlist configuration (ports, IPs, thresholds) from JSON.

    Falls back to sensible defaults if the file is missing or malformed, so
    the tool remains usable without requiring a config file.
    """
    defaults = {
        "watchlist_ports": [4444, 8080],
        "watchlist_ips": [],
        "recent_window_seconds": 3600,
        "failed_login_threshold": 5,
    }
    if not os.path.exists(json_path):
        return defaults
    try:
        with open(json_path) as handle:
            data = json.load(handle)
        defaults.update(data)
        return defaults
    except (json.JSONDecodeError, OSError):
        return defaults


# ---------------------------------------------------------------------------
# Report output
# ---------------------------------------------------------------------------

def write_report_json(report: TriageReport, out_path: str) -> None:
    """Serialize a TriageReport to a JSON file."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as handle:
        json.dump(asdict(report), handle, indent=2, default=str)


def write_report_csv_summary(report: TriageReport, out_path: str) -> None:
    """Write a flat CSV summary of a report (one row per watchlist hit).

    A CSV is inherently row-oriented, so nested detail (like protocol_counts)
    is summarized separately; the JSON export is the full-fidelity format.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["generated_at", "target", "type", "detail"])
        for hit in report.watchlist_hits:
            writer.writerow([report.generated_at, report.target, "watchlist_hit", hit])
        for group in report.duplicate_groups:
            writer.writerow([report.generated_at, report.target, "duplicate_group", group])
        for f in report.recent_files:
            writer.writerow([report.generated_at, report.target, "recent_file", f])
        if not (report.watchlist_hits or report.duplicate_groups or report.recent_files):
            writer.writerow([report.generated_at, report.target, "info", "no findings"])


# ---------------------------------------------------------------------------
# SQLite persistence (scan history)
# ---------------------------------------------------------------------------

@contextmanager
def get_connection(db_path: str = DEFAULT_DB_PATH) -> Iterator[sqlite3.Connection]:
    """Context-managed SQLite connection that also ensures the schema exists."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL,
                target TEXT NOT NULL,
                watchlist_hit_count INTEGER NOT NULL,
                duplicate_group_count INTEGER NOT NULL,
                recent_file_count INTEGER NOT NULL,
                open_port_count INTEGER NOT NULL,
                report_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
        yield conn
    finally:
        conn.close()


def save_report_to_history(report: TriageReport, db_path: str = DEFAULT_DB_PATH) -> int:
    """Insert a completed report into the scan_history table. Returns the new row id."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO scan_history
                (generated_at, target, watchlist_hit_count, duplicate_group_count,
                 recent_file_count, open_port_count, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report.generated_at,
                report.target,
                len(report.watchlist_hits),
                len(report.duplicate_groups),
                len(report.recent_files),
                len(report.open_ports),
                json.dumps(asdict(report), default=str),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def fetch_history(db_path: str = DEFAULT_DB_PATH, limit: int = 10) -> List[sqlite3.Row]:
    """Return the most recent `limit` scan_history rows, newest first."""
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT id, generated_at, target, watchlist_hit_count, duplicate_group_count, "
            "recent_file_count, open_port_count FROM scan_history "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()
