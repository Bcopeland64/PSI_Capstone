import csv
import os
import sqlite3

from .models import Ticket, ticket_from_dict


class TicketRepository:
    """Save and load tickets from a SQLite database."""

    def __init__(self, db_path="data/tickets.db"):
        self.db_path = db_path
        folder = os.path.dirname(db_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self):
   
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT NOT NULL,
                reporter    TEXT NOT NULL,
                severity    TEXT NOT NULL DEFAULT 'unclassified',
                team        TEXT NOT NULL DEFAULT 'unassigned',
                status      TEXT NOT NULL DEFAULT 'open',
                created_at  TEXT NOT NULL,
                due_at      TEXT
            )
            """)
        self._conn.commit()

    def add(self, ticket):
        """Add one ticket and return it with its new ID."""
        values = (ticket.title, ticket.description, ticket.reporter,
                  ticket.severity, ticket.team, ticket.status,
                  ticket.created_at, ticket.due_at)
        cursor = self._conn.execute("""
            INSERT INTO tickets
            (title, description, reporter, severity, team, status, created_at, due_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
        self._conn.commit()
        ticket.ticket_id = cursor.lastrowid
        return ticket

    def update(self, ticket):
        """Save changes to an existing ticket."""
        if ticket.ticket_id is None:
            raise ValueError("Ticket has not been saved yet")
        values = (ticket.title, ticket.description, ticket.reporter,
                  ticket.severity, ticket.team, ticket.status,
                  ticket.created_at, ticket.due_at, ticket.ticket_id)
        self._conn.execute("""
            UPDATE tickets
            SET title=?, description=?, reporter=?, severity=?, team=?,
                status=?, created_at=?, due_at=?
            WHERE ticket_id=?
            """, values)
        self._conn.commit()

    def get(self, ticket_id):
        """Return one ticket by ID, or None if it is missing."""
        row = self._conn.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()
        if row is None:
            return None
        return ticket_from_dict(dict(row))

    def list_all(self):
        """Return all tickets, newest first."""
        rows = self._conn.execute(
            "SELECT * FROM tickets ORDER BY ticket_id DESC"
        ).fetchall()
        tickets = []
        for row in rows:
            tickets.append(ticket_from_dict(dict(row)))
        return tickets

    def delete(self, ticket_id):
        """Delete a ticket and return True if it existed."""
        cursor = self._conn.execute(
            "DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def close(self):
        """Close the database connection."""
        self._conn.close()


def import_csv(path):
    """Read tickets from a CSV file."""
    if not os.path.exists(path):
        raise FileNotFoundError("CSV file not found: " + path)

    tickets = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        required = ["title", "description", "reporter"]
        for column in required:
            if reader.fieldnames is None or column not in reader.fieldnames:
                raise ValueError("CSV is missing the " + column + " column")
        for row in reader:
            tickets.append(ticket_from_dict(row))
    return tickets


def export_csv(tickets, path):
    """Write tickets to a CSV file."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fieldnames = ["ticket_id", "title", "description", "reporter",
                  "severity", "team", "status", "created_at", "due_at"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ticket in tickets:
            writer.writerow(ticket.to_dict())
