"""Persistence layer for SecTriage.

Three storage formats are supported, matching the "Data Persistence"
requirement:

    JSON   -> full-fidelity report export/import (save_report_json / load_report_json)
    CSV    -> flat summary export for spreadsheets (export_summary_csv)
    SQLite -> a running history of triage runs (ReportDatabase)
"""

from __future__ import annotations

import csv
import json
import sqlite3
from typing import List, Optional

from .exceptions import PersistenceError
from .models import TriageReport
from .utils import ensure_parent_dir


def save_report_json(report: TriageReport, path: str) -> None:
    """Write the full report to ``path`` as JSON."""
    ensure_parent_dir(path)
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(report.to_dict(), handle, indent=2)
    except OSError as exc:
        raise PersistenceError(f"Could not write report to '{path}': {exc}") from exc


def load_report_json(path: str) -> dict:
    """Load a previously saved report as a plain dict (for diffing/history)."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise PersistenceError(f"No saved report found at '{path}': {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PersistenceError(f"'{path}' is not valid JSON: {exc}") from exc


def export_summary_csv(report: TriageReport, path: str) -> None:
    """Write a flat, one-row-per-file CSV summary of the report's file hashes."""
    ensure_parent_dir(path)
    try:
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["target", "generated_at", "file_name", "size_bytes", "sha256"])
            for record in report.file_hashes:
                writer.writerow(
                    [report.target, report.generated_at, record.name, record.size_bytes, record.sha256]
                )
    except OSError as exc:
        raise PersistenceError(f"Could not write CSV summary to '{path}': {exc}") from exc


class ReportDatabase:
    """SQLite-backed history of triage runs.

    Lets an analyst answer "how many triage runs have we done, and when",
    and pull back a previous run's raw JSON for comparison -- the
    "historical reporting" piece of the capstone brief.
    """

    def __init__(self, db_path: str = "sectriage_history.db") -> None:
        self.db_path = db_path
        try:
            self._conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as exc:
            raise PersistenceError(f"Could not open database '{db_path}': {exc}") from exc
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    file_count INTEGER NOT NULL,
                    duplicate_group_count INTEGER NOT NULL,
                    report_json TEXT NOT NULL
                )
                """
            )

    def save_run(self, report: TriageReport) -> int:
        """Insert one triage run and return its new row id."""
        payload = json.dumps(report.to_dict())
        with self._conn:
            cursor = self._conn.execute(
                """
                INSERT INTO runs (target, generated_at, file_count, duplicate_group_count, report_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (report.target, report.generated_at, len(report.file_hashes), len(report.duplicate_groups), payload),
            )
        return cursor.lastrowid

    def list_runs(self, limit: int = 10) -> List[sqlite3.Row]:
        """Return the most recent ``limit`` runs (without the full JSON payload)."""
        self._conn.row_factory = sqlite3.Row
        cursor = self._conn.execute(
            """
            SELECT id, target, generated_at, file_count, duplicate_group_count
            FROM runs ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()

    def get_run(self, run_id: int) -> Optional[dict]:
        """Return the full report dict for one historical run, or None."""
        self._conn.row_factory = sqlite3.Row
        cursor = self._conn.execute("SELECT report_json FROM runs WHERE id = ?", (run_id,))
        row = cursor.fetchone()
        return json.loads(row["report_json"]) if row else None

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "ReportDatabase":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
