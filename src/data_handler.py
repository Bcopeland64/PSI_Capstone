"""
data_handler.py
----------------
Persistence layer. Wraps a SQLite database behind a small repository
class (TicketRepository) so the rest of the app never writes raw SQL.
Also provides CSV import/export for interoperability with spreadsheets.
"""

import csv
import sqlite3
from pathlib import Path

from src.models import Ticket

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT NOT NULL,
    description    TEXT NOT NULL,
    category       TEXT NOT NULL,
    reporter       TEXT NOT NULL,
    priority       TEXT NOT NULL,
    status         TEXT NOT NULL,
    priority_score INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);
"""


class DataHandlerError(Exception):
    """Raised for any persistence-layer failure (DB or file I/O)."""


class TicketRepository:
    """
    Repository for ticket persistence backed by SQLite.

    Opens (and lazily creates) a database file at `db_path`. All public
    methods translate low-level sqlite3 errors into DataHandlerError so
    callers only need to catch one exception type.
    """

    def __init__(self, db_path: str = "data/tickets.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute(_SCHEMA)
            self._conn.commit()
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Could not initialize database at '{db_path}': {exc}") from exc

    def add(self, ticket: Ticket) -> Ticket:
        """Insert a new ticket and return it with its assigned ticket_id."""
        try:
            cursor = self._conn.execute(
                """
                INSERT INTO tickets
                    (title, description, category, reporter, priority,
                     status, priority_score, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket.title,
                    ticket.description,
                    ticket.category.value,
                    ticket.reporter,
                    ticket.priority.value,
                    ticket.status.value,
                    ticket.priority_score,
                    ticket.created_at,
                    ticket.updated_at,
                ),
            )
            self._conn.commit()
            ticket.ticket_id = cursor.lastrowid
            return ticket
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to save ticket: {exc}") from exc

    def get(self, ticket_id: int) -> Ticket | None:
        """Fetch a single ticket by id, or None if it doesn't exist."""
        try:
            row = self._conn.execute(
                "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
            ).fetchone()
            return Ticket.from_row(row) if row else None
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to fetch ticket {ticket_id}: {exc}") from exc

    def list_all(self) -> list[Ticket]:
        """Return every ticket in the database."""
        try:
            rows = self._conn.execute("SELECT * FROM tickets").fetchall()
            return [Ticket.from_row(row) for row in rows]
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to list tickets: {exc}") from exc

    def update(self, ticket: Ticket) -> None:
        """Persist changes to an existing ticket (matched by ticket_id)."""
        if ticket.ticket_id is None:
            raise DataHandlerError("Cannot update a ticket that has no ticket_id.")
        try:
            ticket.touch()
            cursor = self._conn.execute(
                """
                UPDATE tickets
                SET title = ?, description = ?, category = ?, reporter = ?,
                    priority = ?, status = ?, priority_score = ?, updated_at = ?
                WHERE ticket_id = ?
                """,
                (
                    ticket.title,
                    ticket.description,
                    ticket.category.value,
                    ticket.reporter,
                    ticket.priority.value,
                    ticket.status.value,
                    ticket.priority_score,
                    ticket.updated_at,
                    ticket.ticket_id,
                ),
            )
            self._conn.commit()
            if cursor.rowcount == 0:
                raise DataHandlerError(f"No ticket found with id {ticket.ticket_id}.")
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to update ticket {ticket.ticket_id}: {exc}") from exc

    def delete(self, ticket_id: int) -> bool:
        """Delete a ticket by id. Returns True if a row was removed."""
        try:
            cursor = self._conn.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
            self._conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to delete ticket {ticket_id}: {exc}") from exc

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()

    # ---- CSV interoperability -------------------------------------------

    def export_csv(self, path: str) -> int:
        """Write all tickets to a CSV file. Returns the number of rows written."""
        tickets = self.list_all()
        try:
            with open(path, "w", newline="", encoding="utf-8") as handle:
                fieldnames = list(tickets[0].as_dict().keys()) if tickets else [
                    "ticket_id", "title", "description", "category", "reporter",
                    "priority", "status", "priority_score", "created_at", "updated_at",
                ]
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                for ticket in tickets:
                    writer.writerow(ticket.as_dict())
            return len(tickets)
        except OSError as exc:
            raise DataHandlerError(f"Failed to export CSV to '{path}': {exc}") from exc

    def import_csv(self, path: str, triage_engine=None) -> int:
        """
        Import tickets from a CSV file with columns:
        title, description, category, reporter (priority/status optional).

        If `triage_engine` is given, priority is auto-scored for each row
        instead of relying on a priority column in the file.
        Returns the number of tickets successfully imported.
        """
        if not Path(path).exists():
            raise DataHandlerError(f"Import file not found: '{path}'")

        imported = 0
        try:
            with open(path, newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    try:
                        from src.models import Category  # local import avoids cycle at module load
                        ticket = Ticket(
                            title=row["title"].strip(),
                            description=row.get("description", "").strip(),
                            category=Category(row.get("category", "OTHER").strip().upper()),
                            reporter=row.get("reporter", "unknown").strip() or "unknown",
                        )
                        if triage_engine:
                            triage_engine.triage(ticket)
                        self.add(ticket)
                        imported += 1
                    except (KeyError, ValueError):
                        # Skip malformed rows but keep processing the rest of the file.
                        continue
            return imported
        except OSError as exc:
            raise DataHandlerError(f"Failed to read CSV '{path}': {exc}") from exc
