#!/usr/bin/env python3
"""
main.py
-------
Entry point for the Capstone Project: an ethical Web Scraper &
Security-Style Analysis Tool.

Usage (from the project root):

    python -m src.main scrape <url> [<url> ...]
    python -m src.main analyze-log <path_to_log_file>
    python -m src.main            # interactive menu

Each mode saves its results under data/ as both CSV and JSON, and
prints a short human-readable summary using `rich` when available.
"""

import argparse
import sys

from src.logic import DataStore, LogAnalyzer, WebScraper

try:
    from rich.console import Console
    from rich.table import Table
    _console = Console()
except ImportError:  # rich is optional -- degrade gracefully to plain print()
    _console = None


def _print(message: str) -> None:
    """Print via rich if available, else plain print()."""
    if _console:
        _console.print(message)
    else:
        print(message)


def run_scrape(urls: list) -> None:
    """Scrape each URL in `urls`, print a summary table, and persist results."""
    records = []
    for url in urls:
        try:
            scraper = WebScraper(url)
            record = scraper.scrape()
            records.append(record)
            _print(f"[green]OK[/green] scraped {url} "
                    f"({record['link_count']} links found)"
                    if _console else f"OK: scraped {url} ({record['link_count']} links)")
        except ValueError as exc:
            _print(f"[red]Invalid URL[/red] '{url}': {exc}" if _console
                    else f"Invalid URL '{url}': {exc}")
        except ConnectionError as exc:
            _print(f"[red]Network error[/red] for '{url}': {exc}" if _console
                    else f"Network error for '{url}': {exc}")

    if not records:
        _print("No pages were successfully scraped. Nothing to save.")
        return

    DataStore.save_to_csv(records, "data/scrape_results.csv")
    DataStore.save_to_json(records, "data/scrape_results.json")
    _print("Saved results to data/scrape_results.csv and data/scrape_results.json")


def run_analyze_log(log_path: str) -> None:
    """Analyze a log file and persist a summary report."""
    try:
        analyzer = LogAnalyzer(log_path)
    except FileNotFoundError as exc:
        _print(f"[red]Error:[/red] {exc}" if _console else f"Error: {exc}")
        return

    report = analyzer.generate_report()

    if _console:
        table = Table(title=f"Log Analysis: {log_path}")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Failed password lines", str(report["failed_password_lines"]))
        for level, count in report["level_tally"].items():
            table.add_row(f"{level} lines", str(count))
        table.add_row("Top IPs", str(report["top_ips"]))
        _console.print(table)
    else:
        print("Log Analysis Report:")
        for key, value in report.items():
            print(f"  {key}: {value}")

    DataStore.save_to_json(report, "data/log_report.json")
    _print("Saved report to data/log_report.json")


def interactive_menu() -> None:
    """Simple text menu for users who run the script with no arguments."""
    while True:
        print("\n=== Capstone Tool: Web Scraper & Analysis ===")
        print("1) Scrape a URL")
        print("2) Analyze a log file")
        print("3) Quit")
        choice = input("Choose an option [1-3]: ").strip()

        if choice == "1":
            url = input("Enter the URL to scrape: ").strip()
            run_scrape([url])
        elif choice == "2":
            path = input("Enter the path to the log file: ").strip()
            run_analyze_log(path)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ethical Web Scraper & Security-Style Analysis Tool"
    )
    subparsers = parser.add_subparsers(dest="command")

    scrape_parser = subparsers.add_parser("scrape", help="Scrape one or more URLs")
    scrape_parser.add_argument("urls", nargs="+", help="One or more URLs to scrape")

    log_parser = subparsers.add_parser("analyze-log", help="Analyze a log file")
    log_parser.add_argument("log_path", help="Path to the log file to analyze")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "scrape":
            run_scrape(args.urls)
        elif args.command == "analyze-log":
            run_analyze_log(args.log_path)
        else:
            interactive_menu()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
