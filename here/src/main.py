import sys

from .data_handler import TicketRepository, export_csv, import_csv
from .logic import TriageEngine
from .models import Ticket
from .utils import ValidationError, require_non_empty

MENU = """
Ticket Triage System
1. New ticket
2. Import tickets from CSV
3. List all tickets
4. View ticket detail
5. Update ticket status
6. Export tickets to CSV
7. Show summary
8. Delete ticket
0. Exit
"""


def read_required(prompt_text, field_name):
    """Ask for text and reject blank input."""
    attempts = 0
    while attempts < 5:
        value = input(prompt_text)
        try:
            return require_non_empty(value, field_name)
        except ValidationError as error:
            print("Invalid input:", error)
        attempts += 1
    print("Too many invalid attempts. Cancelled.")
    return None


def create_ticket(repo, engine):
    """Ask for ticket details, classify the ticket, and save it."""
    title = read_required("Title: ", "Title")
    if title is None:
        return
    description = read_required("Description: ", "Description")
    if description is None:
        return
    reporter = read_required("Reporter name: ", "Reporter")
    if reporter is None:
        return

    ticket = Ticket(title, description, reporter)
    engine.triage(ticket)
    repo.add(ticket)
    print("Ticket", ticket.ticket_id, "created")
    print("Severity:", ticket.severity)
    print("Team:", ticket.team)
    print("Due:", ticket.due_at)


def import_from_csv(repo, engine):
    """Read tickets from a CSV file and save them."""
    path = input("CSV path: ").strip()
    try:
        tickets = import_csv(path)
        count = 0
        for ticket in tickets:
            ticket.ticket_id = None
            engine.triage(ticket)
            repo.add(ticket)
            count += 1
        print("Imported", count, "ticket(s).")
    except (FileNotFoundError, ValueError) as error:
        print("Import failed:", error)


def list_tickets(repo):
    """Print a short line for every saved ticket."""
    tickets = repo.list_all()
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        print("ID:", ticket.ticket_id,
              "| Title:", ticket.title,
              "| Severity:", ticket.severity,
              "| Team:", ticket.team,
              "| Status:", ticket.status,
              "| Due:", ticket.due_at)


def read_ticket_id():
    """Read a ticket ID from the user."""
    raw = input("Ticket ID: ").strip()
    try:
        return int(raw)
    except ValueError:
        print("Ticket ID must be a number.")
        return None


def view_detail(repo):
    """Print every field for one ticket."""
    ticket_id = read_ticket_id()
    if ticket_id is None:
        return
    ticket = repo.get(ticket_id)
    if ticket is None:
        print("No ticket with ID", ticket_id)
        return
    details = ticket.to_dict()
    for key in details:
        print(key + ":", details[key])


def update_status(repo):
    """Change the status of one ticket."""
    ticket_id = read_ticket_id()
    if ticket_id is None:
        return
    ticket = repo.get(ticket_id)
    if ticket is None:
        print("No ticket with ID", ticket_id)
        return

    new_status = input("New status (open/in_progress/resolved/closed): ").strip()
    try:
        ticket.mark_status(new_status)
        repo.update(ticket)
        print("Ticket", ticket_id, "updated.")
    except ValueError as error:
        print("Could not update ticket:", error)


def export_to_csv(repo):
    """Write all saved tickets to a CSV file."""
    path = input("Export path: ").strip()
    try:
        tickets = repo.list_all()
        export_csv(tickets, path)
        print("Exported", len(tickets), "ticket(s).")
    except OSError as error:
        print("Export failed:", error)


def show_summary(repo):
    """Print counts for the saved tickets."""
    tickets = repo.list_all()
    summary = TriageEngine.summarize(tickets)
    print("Total tickets:", summary["total"])
    print("Overdue:", summary["overdue"])
    print("By severity:", summary["by_severity"])
    print("By team:", summary["by_team"])
    print("By status:", summary["by_status"])


def delete_ticket(repo):
    """Delete one ticket by ID."""
    ticket_id = read_ticket_id()
    if ticket_id is None:
        return
    if repo.delete(ticket_id):
        print("Ticket", ticket_id, "deleted.")
    else:
        print("No ticket with ID", ticket_id)


def run():
    """Run the menu until the user chooses Exit."""
    repo = TicketRepository()
    engine = TriageEngine()

    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "1":
                create_ticket(repo, engine)
            elif choice == "2":
                import_from_csv(repo, engine)
            elif choice == "3":
                list_tickets(repo)
            elif choice == "4":
                view_detail(repo)
            elif choice == "5":
                update_status(repo)
            elif choice == "6":
                export_to_csv(repo)
            elif choice == "7":
                show_summary(repo)
            elif choice == "8":
                delete_ticket(repo)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Not a valid option.")
    except (KeyboardInterrupt, EOFError):
        print("Goodbye!")
    finally:
        repo.close()


if __name__ == "__main__":
    sys.exit(run() or 0)
