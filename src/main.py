"""Command-line entry point for the Security Incident Triage Tool."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.data_handler import DataHandler
from src.logic import TriageEngine
from src.models import Incident


console = Console()
DEFAULT_CSV = "data/sample_incidents.csv"
DEFAULT_DATABASE = "data/triage.db"


def display_statistics(statistics: dict) -> None:
    """Display triage summary statistics."""
    table = Table(title="Security Triage Report")
    table.add_column("Category")
    table.add_column("Count", justify="right")

    table.add_row("Total Incidents", str(statistics["total"]))
    table.add_row("Critical", str(statistics["critical"]))
    table.add_row("High", str(statistics["high"]))
    table.add_row("Medium", str(statistics["medium"]))
    table.add_row("Low", str(statistics["low"]))

    console.print(table)

    attack_table = Table(title="Attack Type Distribution")
    attack_table.add_column("Attack Type")
    attack_table.add_column("Count", justify="right")

    for attack_type, count in sorted(
        statistics["attack_types"].items()
    ):
        attack_table.add_row(attack_type, str(count))

    console.print(attack_table)


def display_incident(row: tuple) -> None:
    """Display one stored incident."""
    labels = [
        "Incident ID",
        "Timestamp",
        "Source IP",
        "Destination IP",
        "Attack Type",
        "Username",
        "Description",
        "Severity",
        "Score",
    ]

    table = Table(title=f"Incident {row[0]}")
    table.add_column("Field")
    table.add_column("Value")

    for label, value in zip(labels, row):
        table.add_row(label, str(value))

    console.print(table)


def process_file(
    csv_path: str,
    handler: DataHandler,
    engine: TriageEngine,
) -> None:
    """Process a CSV file and persist valid incidents."""
    try:
        dataframe = handler.load_csv(csv_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Input error:[/red] {exc}")
        return

    incidents: list[Incident] = []
    skipped = 0

    for row_number, row in enumerate(
        dataframe.to_dict(orient="records"),
        start=2,
    ):
        try:
            incident = engine.create_incident(row)
            incidents.append(incident)
        except (ValueError, TypeError) as exc:
            skipped += 1
            console.print(
                f"[yellow]Skipped CSV row {row_number}:[/yellow] {exc}"
            )

    if not incidents:
        console.print(
            "[red]No valid incidents were found in the input file.[/red]"
        )
        return

    saved = handler.save_incidents(incidents)
    statistics = engine.analyze(incidents)

    console.print(
        Panel.fit(
            f"Processed: {len(incidents)}\n"
            f"Skipped: {skipped}\n"
            f"Saved to SQLite: {saved}",
            title="Processing Complete",
        )
    )
    display_statistics(statistics)


def search_incident(handler: DataHandler) -> None:
    """Prompt for an ID and display the matching incident."""
    incident_id = input("Enter Incident ID: ").strip()

    if not incident_id:
        console.print("[red]Incident ID cannot be empty.[/red]")
        return

    result = handler.search_incident(incident_id)

    if result is None:
        console.print(
            f"[yellow]Incident '{incident_id}' was not found.[/yellow]"
        )
        return

    display_incident(result)


def list_incidents(handler: DataHandler) -> None:
    """Display all stored incidents."""
    rows = handler.get_all_incidents()

    if not rows:
        console.print("[yellow]No incidents are stored yet.[/yellow]")
        return

    table = Table(title="Stored Security Incidents")
    table.add_column("ID")
    table.add_column("Timestamp")
    table.add_column("Attack")
    table.add_column("Source IP")
    table.add_column("Severity")
    table.add_column("Score")

    for row in rows:
        table.add_row(
            str(row[0]),
            str(row[1]),
            str(row[4]),
            str(row[2]),
            str(row[7]),
            str(row[8]),
        )

    console.print(table)


def export_report(handler: DataHandler) -> None:
    """Export stored incidents to a CSV report."""
    output = input(
        "Output path (default: data/triage_report.csv): "
    ).strip()

    output_path = output or "data/triage_report.csv"

    try:
        count = handler.export_csv(output_path)
        console.print(
            f"[green]Exported {count} incidents to "
            f"{Path(output_path)}[/green]"
        )
    except OSError as exc:
        console.print(f"[red]Export error:[/red] {exc}")


def main() -> None:
    """Run the interactive CLI application."""
    handler = DataHandler(DEFAULT_DATABASE)
    engine = TriageEngine()

    try:
        handler.initialize_database()
    except OSError as exc:
        console.print(f"[red]Database error:[/red] {exc}")
        return

    console.print(
        Panel.fit(
            "Security Incident Triage Tool",
            subtitle="Python Capstone Project",
        )
    )

    while True:
        console.print(
            """
[bold]Menu[/bold]

1. Process CSV incidents
2. Search incident
3. List stored incidents
4. Export stored incidents to CSV
5. Exit
"""
        )

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            csv_path = input(
                f"CSV path (default: {DEFAULT_CSV}): "
            ).strip()
            process_file(
                csv_path or DEFAULT_CSV,
                handler,
                engine,
            )

        elif choice == "2":
            search_incident(handler)

        elif choice == "3":
            list_incidents(handler)

        elif choice == "4":
            export_report(handler)

        elif choice == "5":
            console.print("[cyan]Goodbye![/cyan]")
            break

        else:
            console.print(
                "[red]Invalid choice. Please enter a number from 1 to 5.[/red]"
            )


if __name__ == "__main__":
    main()
