"""CSV ingestion and SQLite persistence."""

import csv
import sqlite3
from pathlib import Path

import pandas as pd

from src.models import Incident


class DataHandler:
    """Handle input files and persistent incident storage."""

    TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            destination_ip TEXT NOT NULL,
            attack_type TEXT NOT NULL,
            username TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """

    def __init__(self, database_path: str = "data/triage.db") -> None:
        """Initialize the data handler."""
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def initialize_database(self) -> None:
        """Create the SQLite table when it does not already exist."""
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(self.TABLE_SQL)
            connection.commit()

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file into a DataFrame."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"CSV path is not a file: {file_path}")

        try:
            dataframe = pd.read_csv(path)
        except pd.errors.EmptyDataError as exc:
            raise ValueError("The CSV file is empty.") from exc
        except pd.errors.ParserError as exc:
            raise ValueError("The CSV file is malformed.") from exc

        if dataframe.empty:
            raise ValueError("The CSV file contains no records.")

        return dataframe

    def save_incidents(self, incidents: list[Incident]) -> int:
        """Insert or replace incidents in SQLite and return count saved."""
        if not incidents:
            return 0

        rows = [
            (
                incident.incident_id,
                incident.timestamp.isoformat(sep=" "),
                incident.source_ip,
                incident.destination_ip,
                incident.attack_type,
                incident.username,
                incident.description,
                incident.severity,
                incident.score,
            )
            for incident in incidents
        ]

        with sqlite3.connect(self.database_path) as connection:
            connection.executemany(
                """
                INSERT OR REPLACE INTO incidents
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()

        return len(rows)

    def get_all_incidents(self) -> list[tuple]:
        """Return all stored incidents ordered by newest timestamp."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(
                """
                SELECT incident_id, timestamp, source_ip,
                       destination_ip, attack_type, username,
                       description, severity, score
                FROM incidents
                ORDER BY timestamp DESC
                """
            )
            return cursor.fetchall()

    def search_incident(self, incident_id: str) -> tuple | None:
        """Return one incident by ID, or None when not found."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(
                """
                SELECT incident_id, timestamp, source_ip,
                       destination_ip, attack_type, username,
                       description, severity, score
                FROM incidents
                WHERE incident_id = ?
                """,
                (incident_id,),
            )
            return cursor.fetchone()

    def export_csv(self, output_path: str = "data/triage_report.csv") -> int:
        """Export stored incidents to CSV and return exported row count."""
        rows = self.get_all_incidents()
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        headers = [
            "incident_id",
            "timestamp",
            "source_ip",
            "destination_ip",
            "attack_type",
            "username",
            "description",
            "severity",
            "score",
        ]

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        return len(rows)
