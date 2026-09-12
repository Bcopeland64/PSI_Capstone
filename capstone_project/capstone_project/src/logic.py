"""Core triage logic: traffic log analysis, hash verification, API lookups.

This module ties utils.py (primitives) and models.py (data + storage)
together into the operations the CLI in main.py calls.
"""

from __future__ import annotations

import csv
from collections import Counter

import requests

from .models import Connection, FileHashRecord, PortCheckResult, TriageDatabase
from .utils import hash_file, port_status

DEFAULT_SUSPICIOUS_PORTS = {4444, 31337, 6667}


def load_connections(csv_path: str) -> list[Connection]:
    """Read a traffic CSV into a list of Connection objects.

    Rows that don't parse cleanly are skipped with a warning printed to
    the console, rather than crashing the whole report.
    """
    connections: list[Connection] = []
    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row_number, row in enumerate(reader, start=2):  # header is line 1
                try:
                    connections.append(Connection.from_csv_row(row))
                except ValueError as exc:
                    print(f"  [warning] skipping row {row_number}: {exc}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Traffic log not found: '{csv_path}'. Check the path and try again."
        )
    return connections


def top_talkers_by_bytes(connections: list[Connection], top_n: int = 5) -> list[tuple[str, int]]:
    """Return the top_n src_ip addresses ranked by total bytes transferred."""
    totals: Counter = Counter()
    for conn in connections:
        totals[conn.src_ip] += conn.num_bytes
    return totals.most_common(top_n)


def port_connection_counts(connections: list[Connection], top_n: int = 5) -> list[tuple[int, int]]:
    """Return the top_n destination ports ranked by connection count."""
    counts: Counter = Counter(conn.dst_port for conn in connections)
    return counts.most_common(top_n)


def flag_suspicious_ports(
    connections: list[Connection], suspicious_ports: set[int] = None
) -> list[Connection]:
    """Return every connection whose destination port is on the watchlist."""
    watchlist = suspicious_ports if suspicious_ports is not None else DEFAULT_SUSPICIOUS_PORTS
    return [conn for conn in connections if conn.dst_port in watchlist]


def build_traffic_report(csv_path: str, suspicious_ports: set[int] = None) -> dict:
    """Load a traffic log and return a structured summary report.

    Returned dict keys: total_connections, top_talkers, top_ports, flagged.
    Kept as a dict (rather than printed directly) so main.py controls
    formatting and other code could reuse the data (e.g. for tests).
    """
    connections = load_connections(csv_path)
    return {
        "total_connections": len(connections),
        "top_talkers": top_talkers_by_bytes(connections),
        "top_ports": port_connection_counts(connections),
        "flagged": flag_suspicious_ports(connections, suspicious_ports),
    }


def check_file_integrity(path: str, db: TriageDatabase) -> dict:
    """Hash a file, compare it against the last stored hash, and save the new one.

    Returns a dict describing the outcome: status is 'first_seen' (no prior
    record), 'match' (unchanged), or 'mismatch' (file changed since last check).
    """
    current_hash = hash_file(path)
    previous = db.get_latest_hash(path)
    db.save_hash_record(FileHashRecord.new(path, current_hash))

    if previous is None:
        return {"status": "first_seen", "sha256": current_hash}
    if previous.sha256 == current_hash:
        return {"status": "match", "sha256": current_hash}
    return {
        "status": "mismatch",
        "sha256": current_hash,
        "previous_sha256": previous.sha256,
        "previous_recorded_at": previous.recorded_at,
    }


def check_and_record_port(host: str, port: int, db: TriageDatabase) -> PortCheckResult:
    """Check a host:port, persist the result, and return it."""
    status = port_status(host, port)
    result = PortCheckResult.new(host, port, status)
    db.save_port_check(result)
    return result


def fetch_random_uuid(timeout: float = 5.0) -> str:
    """Fetch a fresh UUID from httpbin as a lightweight external-API demo.

    Raises requests.RequestException on network failure or a non-2xx
    status, so the CLI can catch it and report a clean error message.
    """
    response = requests.get("https://httpbin.org/uuid", timeout=timeout)
    response.raise_for_status()
    return response.json()["uuid"]
