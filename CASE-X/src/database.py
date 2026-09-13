import sqlite3
from pathlib import Path
from typing import Iterable


class Database:
    """Small SQLite data layer for CASE-X."""

    def __init__(self, db_path: str = "data/casex.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self) -> None:
        with self.connection:
            self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                victim TEXT NOT NULL,
                location TEXT NOT NULL,
                case_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
            );

            CREATE TABLE IF NOT EXISTS suspects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                occupation TEXT NOT NULL,
                relationship TEXT NOT NULL,
                alibi TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                suspect_id INTEGER,
                evidence_type TEXT NOT NULL,
                description TEXT NOT NULL,
                reliability INTEGER NOT NULL CHECK(reliability BETWEEN 1 AND 100),
                FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE CASCADE,
                FOREIGN KEY(suspect_id) REFERENCES suspects(id) ON DELETE SET NULL
            );
            """)

    def execute(self, query: str, params: Iterable = ()):
        with self.connection:
            return self.connection.execute(query, tuple(params))

    def fetchall(self, query: str, params: Iterable = ()):
        return self.connection.execute(query, tuple(params)).fetchall()

    def fetchone(self, query: str, params: Iterable = ()):
        return self.connection.execute(query, tuple(params)).fetchone()

    def close(self) -> None:
        self.connection.close()
