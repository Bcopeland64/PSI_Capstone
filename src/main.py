"""
main.py
-------
Command-line entry point for the Support Ticket Triage System.

Run with:  python -m src.main

Presents a menu-driven interface for logging tickets, letting the
TriageEngine auto-assign a priority, managing ticket status, and
viewing reports. All I/O errors and validation errors are caught here
so the app never crashes on bad input.
"""

import sys

from src.data_handler import DataHandlerError, TicketRepository
from src.logic import TriageEngine, sort_by_urgency, summarize
from src.models import Category, Priority, Status, Ticket
from src.utils import (
    ValidationError,
    parse_category,
    parse_positive_int,
    parse_status,
    priority_badge,
    require_non_empty,
    truncate,
)

MENU = """
==================== SUPPORT TICKET TRIAGE ====================
 1. Log a new ticket (auto-triaged)
 2. List all tickets (sorted by urgency)
 3. View ticket details
 4. Update ticket status
 5. Show summary report
 6. Import tickets from CSV
 7. Export tickets to CSV
 8. Delete a ticket
 9. Exit
=================================================================
"""


def prompt(label: str) -> str:
    """Thin wrapper around input() so it's easy to mock in tests."""
    return input(label)


def add_ticket(repo: TicketRepository, engine: TriageEngine) -> None:
    try:
        title = require_non_empty(prompt("Title: "), "Title")
        description = require_non_empty(prompt("Description: "), "Description")
        print(f"Categories: {', '.join(Category.values())}")
        category = parse_category(prompt("Category: "))
        reporter = require_non_empty(prompt("Reporter name/email: "), "Reporter")

        ticket = Ticket(title=title, description=description, category=category, reporter=reporter)
        engine.triage(ticket)
        repo.add(ticket)

        print(
            f"\n✔ Ticket #{ticket.ticket_id} logged. "
            f"Auto-assigned priority: {ticket.priority.value} (score {ticket.priority_score})."
        )
    except ValidationError as exc:
        print(f"✘ Input error: {exc}")
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def list_tickets(repo: TicketRepository) -> None:
    try:
        tickets = sort_by_urgency(repo.list_all())
        if not tickets:
            print("No tickets logged yet.")
            return
        print(f"\n{'ID':<4} {'Priority':<8} {'Status':<12} {'Category':<16} {'Title':<40}")
        print("-" * 84)
        for ticket in tickets:
            print(
                f"{ticket.ticket_id:<4} {priority_badge(ticket.priority):<8} "
                f"{ticket.status.value:<12} {ticket.category.value:<16} {truncate(ticket.title):<40}"
            )
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def view_ticket(repo: TicketRepository) -> None:
    try:
        ticket_id = parse_positive_int(prompt("Ticket ID: "), "Ticket ID")
        ticket = repo.get(ticket_id)
        if not ticket:
            print(f"No ticket found with id {ticket_id}.")
            return
        for key, value in ticket.as_dict().items():
            print(f"  {key:<15}: {value}")
    except ValidationError as exc:
        print(f"✘ Input error: {exc}")
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def update_status(repo: TicketRepository) -> None:
    try:
        ticket_id = parse_positive_int(prompt("Ticket ID: "), "Ticket ID")
        ticket = repo.get(ticket_id)
        if not ticket:
            print(f"No ticket found with id {ticket_id}.")
            return
        print(f"Valid statuses: {', '.join(Status.values())}")
        new_status = parse_status(prompt("New status: "))
        ticket.status = new_status
        repo.update(ticket)
        print(f"✔ Ticket #{ticket_id} status updated to {new_status.value}.")
    except ValidationError as exc:
        print(f"✘ Input error: {exc}")
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def show_summary(repo: TicketRepository) -> None:
    try:
        stats = summarize(repo.list_all())
        print(f"\nTotal tickets: {stats['total']}")
        print(f"Average urgency score: {stats['avg_score']}")
        print(f"By priority: {stats['by_priority']}")
        print(f"By status:   {stats['by_status']}")
        print(f"By category: {stats['by_category']}")
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def import_csv(repo: TicketRepository, engine: TriageEngine) -> None:
    try:
        path = require_non_empty(prompt("CSV path to import: "), "Path")
        count = repo.import_csv(path, triage_engine=engine)
        print(f"✔ Imported {count} ticket(s) from '{path}'.")
    except (ValidationError, DataHandlerError) as exc:
        print(f"✘ {exc}")


def export_csv(repo: TicketRepository) -> None:
    try:
        path = require_non_empty(prompt("CSV path to export to: "), "Path")
        count = repo.export_csv(path)
        print(f"✔ Exported {count} ticket(s) to '{path}'.")
    except (ValidationError, DataHandlerError) as exc:
        print(f"✘ {exc}")


def delete_ticket(repo: TicketRepository) -> None:
    try:
        ticket_id = parse_positive_int(prompt("Ticket ID to delete: "), "Ticket ID")
        confirm = prompt(f"Type 'yes' to confirm deleting ticket #{ticket_id}: ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return
        deleted = repo.delete(ticket_id)
        print(f"✔ Deleted." if deleted else f"No ticket found with id {ticket_id}.")
    except ValidationError as exc:
        print(f"✘ Input error: {exc}")
    except DataHandlerError as exc:
        print(f"✘ Storage error: {exc}")


def run() -> None:
    """Main interactive loop. Keeps running until the user chooses Exit."""
    repo = TicketRepository()
    engine = TriageEngine()

    actions = {
        "1": lambda: add_ticket(repo, engine),
        "2": lambda: list_tickets(repo),
        "3": lambda: view_ticket(repo),
        "4": lambda: update_status(repo),
        "5": lambda: show_summary(repo),
        "6": lambda: import_csv(repo, engine),
        "7": lambda: export_csv(repo),
        "8": lambda: delete_ticket(repo),
    }

    try:
        while True:
            print(MENU)
            choice = prompt("Choose an option (1-9): ").strip()
            if choice == "9":
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("✘ Please enter a number from 1 to 9.")
                continue
            action()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting safely.")
    finally:
        repo.close()


if __name__ == "__main__":
    sys.exit(run() or 0)
