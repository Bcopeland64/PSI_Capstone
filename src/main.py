"""Command-line entry point for the cybersecurity triage tool."""

import argparse
import sys

from .logic import run_triage
from .report import export_csv, print_report


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a read-only end-to-end file triage report."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default="data/sample_evidence",
        help="Target folder to inspect.",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=600,
        help="Recent-file window in seconds (default: 600).",
    )
    parser.add_argument(
        "--output",
        default="output/triage_report.csv",
        help="CSV output path.",
    )
    return parser.parse_args()


def main():
    """Run the triage workflow and handle user errors gracefully."""
    args = parse_args()

    if args.window < 0:
        print("Error: --window must be 0 or greater.")
        return 1

    try:
        report = run_triage(args.folder, args.window)
        print_report(report)
        export_csv(report, args.output)
        print(f"\nCSV report saved to: {args.output}")
        return 0

    except NotADirectoryError as error:
        print(f"Error: {error}")
        return 1
    except PermissionError as error:
        print(f"Error: permission denied: {error}")
        return 1
    except OSError as error:
        print(f"Error: operating-system error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
