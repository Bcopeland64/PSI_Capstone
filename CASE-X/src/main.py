from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .database import Database
from .logic import InvestigationService
from .reporting import create_score_chart, export_case_csv
from .utils import pause, prompt_date, prompt_int, prompt_nonempty

console = Console()


def seed_demo(service):
    """Create a realistic demo case on first run."""
    if service.list_cases():
        return

    case_id = service.add_case(
        "The Vienna Gallery Incident",
        "Daniel Weber",
        "Vienna",
        "2026-08-14",
    )
    a = service.add_suspect(
        case_id, "Alex Morgan", 31, "Security Consultant", "Business partner",
        "Claims he was at a nearby café."
    )
    b = service.add_suspect(
        case_id, "Mark Fischer", 42, "Gallery Manager", "Employee",
        "Says he left the gallery at 21:30."
    )
    c = service.add_suspect(
        case_id, "Sarah Klein", 28, "Journalist", "Friend",
        "Was interviewing another witness."
    )
    service.add_evidence(
        case_id, "Fingerprint", "Partial fingerprint found on a display case.", 88, a
    )
    service.add_evidence(
        case_id, "Location", "Phone metadata places suspect near the scene.", 79, a
    )
    service.add_evidence(
        case_id, "Witness", "Witness noticed a person matching his description.", 62, b
    )
    service.add_evidence(
        case_id, "Access Log", "Badge used after stated departure time.", 91, b
    )
    service.add_evidence(
        case_id, "Interview", "Timeline contains an unexplained gap.", 45, c
    )


def show_banner():
    console.print(
        Panel.fit(
            "[bold]CASE-X[/bold]\n"
            "Intelligent Criminal Investigation & Evidence Analysis System",
            border_style="bright_blue",
        )
    )


def choose_case(service):
    cases = service.list_cases()
    if not cases:
        console.print("[yellow]No cases available.[/yellow]")
        return None

    table = Table(title="Cases")
    for col in ("ID", "Title", "Victim", "Location", "Date", "Status"):
        table.add_column(col)
    for c in cases:
        table.add_row(
            str(c["id"]), c["title"], c["victim"], c["location"],
            c["case_date"], c["status"]
        )
    console.print(table)
    case_id = prompt_int("Case ID: ", 1)
    if not service.get_case(case_id):
        console.print("[red]Case not found.[/red]")
        return None
    return case_id


def show_dashboard(service, case_id):
    case = service.get_case(case_id)
    data = service.dashboard_data(case_id)

    console.print(
        Panel(
            f"[bold]{case['title']}[/bold]\n"
            f"Victim: {case['victim']} | Location: {case['location']} | "
            f"Date: {case['case_date']}",
            title=f"Case #{case_id}",
        )
    )

    table = Table(title="Suspect Ranking")
    table.add_column("Rank")
    table.add_column("Suspect")
    table.add_column("Score")
    table.add_column("Evidence")
    for rank, row in enumerate(data["scores"], 1):
        table.add_row(
            str(rank), row["name"], f"{row['score']}%", str(row["evidence_count"])
        )
    console.print(table)
    console.print(
        f"Evidence: {data['evidence_count']} | "
        f"Average reliability: {data['average_reliability']}"
    )


def add_case(service):
    console.print("[bold]Create New Case[/bold]")
    title = prompt_nonempty("Case title: ")
    victim = prompt_nonempty("Victim name: ")
    location = prompt_nonempty("Location: ")
    case_date = prompt_date("Date (YYYY-MM-DD): ")
    case_id = service.add_case(title, victim, location, case_date)
    console.print(f"[green]Created case #{case_id}.[/green]")


def add_suspect(service):
    case_id = choose_case(service)
    if case_id is None:
        return
    name = prompt_nonempty("Name: ")
    age = prompt_int("Age: ", 1, 120)
    occupation = prompt_nonempty("Occupation: ")
    relationship = prompt_nonempty("Relationship to victim: ")
    alibi = prompt_nonempty("Alibi: ")
    suspect_id = service.add_suspect(
        case_id, name, age, occupation, relationship, alibi
    )
    console.print(f"[green]Added suspect #{suspect_id}.[/green]")


def add_evidence(service):
    case_id = choose_case(service)
    if case_id is None:
        return
    suspects = service.get_suspects(case_id)
    if not suspects:
        console.print("[yellow]Add a suspect first.[/yellow]")
        return

    table = Table(title="Suspects")
    table.add_column("ID")
    table.add_column("Name")
    for s in suspects:
        table.add_row(str(s["id"]), s["name"])
    console.print(table)

    suspect_id = prompt_int("Suspect ID linked to evidence: ", 1)
    if not any(s["id"] == suspect_id for s in suspects):
        console.print("[red]Invalid suspect ID.[/red]")
        return

    evidence_type = prompt_nonempty("Evidence type: ")
    description = prompt_nonempty("Description: ")
    reliability = prompt_int("Reliability (1-100): ", 1, 100)
    evidence_id = service.add_evidence(
        case_id, evidence_type, description, reliability, suspect_id
    )
    console.print(f"[green]Added evidence #{evidence_id}.[/green]")


def reports(service):
    case_id = choose_case(service)
    if case_id is None:
        return
    csv_path = export_case_csv(service, case_id)
    chart_path = create_score_chart(service, case_id)
    console.print(f"[green]CSV report:[/green] {csv_path}")
    if chart_path:
        console.print(f"[green]Chart:[/green] {chart_path}")


def main():
    db = Database()
    service = InvestigationService(db)
    seed_demo(service)

    try:
        while True:
            show_banner()
            console.print(
                "\n[1] View Case Dashboard\n"
                "[2] Create New Case\n"
                "[3] Add Suspect\n"
                "[4] Add Evidence\n"
                "[5] Export Reports\n"
                "[6] Exit"
            )
            choice = input("\nSelect: ").strip()

            try:
                if choice == "1":
                    case_id = choose_case(service)
                    if case_id:
                        show_dashboard(service, case_id)
                    pause()
                elif choice == "2":
                    add_case(service)
                    pause()
                elif choice == "3":
                    add_suspect(service)
                    pause()
                elif choice == "4":
                    add_evidence(service)
                    pause()
                elif choice == "5":
                    reports(service)
                    pause()
                elif choice == "6":
                    console.print("[cyan]Goodbye, Investigator.[/cyan]")
                    break
                else:
                    console.print("[red]Choose a number from 1 to 6.[/red]")
            except Exception as exc:
                console.print(f"[red]Operation failed safely: {exc}[/red]")
                pause()
    finally:
        db.close()


if __name__ == "__main__":
    main()
