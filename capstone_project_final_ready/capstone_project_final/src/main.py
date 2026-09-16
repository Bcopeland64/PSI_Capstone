"""Command-line entry point for the End-to-End Security Triage Script."""

import argparse
import os
import sys

from rich.console import Console
from rich.table import Table

from .data_handler import (
    read_log_file,
    save_events_csv,
    save_json,
    save_summary_csv,
)
from .logic import LogAnalyzer
from .utils import validate_file_path, validate_threshold


console = Console()


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Perform basic SSH authentication log triage."
    )
    parser.add_argument(
        "log_file",
        nargs="?",
        default="data/sample_auth.log",
        help="Path to the SSH authentication log.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=5,
        help="Minimum failed attempts from one IP to flag it.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="reports/triage_report.json",
        help="Path for the JSON report.",
    )
    return parser


def display_result(result) -> None:
    """Display the triage result in a readable terminal table."""
    console.print("\n[bold]END-TO-END SECURITY TRIAGE[/bold]\n")

    summary = Table(title="Triage Summary")
    summary.add_column("Metric")
    summary.add_column("Value")

    metrics = [
        ("Total Events", result.total_events),
        ("Failed Logins", result.failed_logins),
        ("Successful Logins", result.successful_logins),
        ("Other Events", result.other_events),
        ("Unique IPs", result.unique_ips),
        ("Suspicious Events", result.suspicious_event_count),
    ]

    for name, value in metrics:
        summary.add_row(name, str(value))

    console.print(summary)

    suspicious = Table(title="Suspicious Source IPs")
    suspicious.add_column("Source IP")
    suspicious.add_column("Failed Attempts")

    if result.suspicious_ips:
        for ip, count in result.suspicious_ips.items():
            suspicious.add_row(ip, str(count))
    else:
        suspicious.add_row("None detected", "-")

    console.print(suspicious)


def main() -> int:
    """Run the complete triage workflow."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        log_file = validate_file_path(args.log_file)
        threshold = validate_threshold(args.threshold)

        console.print("[bold]Loading log file...[/bold]")
        lines = read_log_file(log_file)

        if not lines:
            raise ValueError("The supplied log file is empty.")

        analyzer = LogAnalyzer(threshold=threshold)
        result = analyzer.analyze(lines)

        save_json(result.to_dict(), args.output)

        event_csv = os.path.splitext(args.output)[0] + "_events.csv"
        summary_csv = os.path.splitext(args.output)[0] + "_summary.csv"

        save_events_csv(
            [event.to_dict() for event in analyzer.events],
            event_csv,
        )
        save_summary_csv(result.to_dict(), summary_csv)

        display_result(result)

        console.print(f"\nJSON report : {args.output}")
        console.print(f"Events CSV  : {event_csv}")
        console.print(f"Summary CSV : {summary_csv}")

    except (
        FileNotFoundError,
        PermissionError,
        ValueError,
        OSError,
    ) as exc:
        console.print(f"[bold]Error:[/bold] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
