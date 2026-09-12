"""Data models and persistence for the Triage Toolkit.

This module defines the core objects the toolkit works with (a network
connection record and a file-hash record) plus a small SQLite wrapper,
`TriageDatabase`, that gives the app durable storage between runs.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Connection:
    """A single row from a network traffic log.

    Encapsulates one connection record and knows how to build itself
    from a raw csv.DictReader row (which always yields strings).
    """

    timestamp: str
    src_ip: str
    dst_port: int
    protocol: str
    num_bytes: int

    @classmethod
    def from_csv_row(cls, row: dict) -> "Connection":
        """Build a Connection from a csv.DictReader row.

        Raises ValueError if required fields are missing or malformed,
        so callers can skip/report bad rows instead of crashing.
        """
        try:
            return cls(
                timestamp=row["timestamp"],
                src_ip=row["src_ip"],
                dst_port=int(row["dst_port"]),
                protocol=row["protocol"],
                num_bytes=int(row["bytes"]),
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f"Malformed connection row {row!r}: {exc}") from exc


@dataclass
class FileHashRecord:
    """A recorded SHA-256 hash for a file at a point in time."""

    path: str
    sha256: str
    recorded_at: str

    @classmethod
    def new(cls, path: str, sha256: str) -> "FileHashRecord":
        """Create a record stamped with the current UTC time."""
        return cls(path=path, sha256=sha256, recorded_at=datetime.now(timezone.utc).isoformat())


@dataclass
class PortCheckResult:
    """The outcome of checking a single host:port."""

    host: str
    port: int
    status: str  # "open" or "closed"
    checked_at: str

    @classmethod
    def new(cls, host: str, port: int, status: str) -> "PortCheckResult":
        return cls(host=host, port=port, status=status, checked_at=datetime.now(timezone.utc).isoformat())


class TriageDatabase:
    """Thin SQLite wrapper providing durable storage for toolkit results.

    Kept deliberately small: a handful of tables, plain SQL, and one
    connection per instance. Using ``with TriageDatabase(path) as db:``
    ensures the connection is always closed.
    """

    def __init__(self, db_path: str = "data/triage.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS file_hashes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS port_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    host TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    checked_at TEXT NOT NULL
                )
                """
            )

    def save_hash_record(self, record: FileHashRecord) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO file_hashes (path, sha256, recorded_at) VALUES (?, ?, ?)",
                (record.path, record.sha256, record.recorded_at),
            )

    def get_latest_hash(self, path: str) -> FileHashRecord | None:
        """Return the most recently stored hash for a path, or None."""
        cur = self._conn.execute(
            "SELECT path, sha256, recorded_at FROM file_hashes "
            "WHERE path = ? ORDER BY id DESC LIMIT 1",
            (path,),
        )
        row = cur.fetchone()
        return FileHashRecord(**row) if row else None

    def save_port_check(self, result: PortCheckResult) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO port_checks (host, port, status, checked_at) VALUES (?, ?, ?, ?)",
                (result.host, result.port, result.status, result.checked_at),
            )

    def recent_port_checks(self, limit: int = 10) -> list[sqlite3.Row]:
        cur = self._conn.execute(
            "SELECT host, port, status, checked_at FROM port_checks "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "TriageDatabase":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
