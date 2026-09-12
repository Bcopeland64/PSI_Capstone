"""Triage Toolkit — CLI entry point.

Run with:  python -m src.main
(from the capstone_project/ root, so the relative imports resolve)

A menu-driven CLI that wraps the toolkit's four capabilities:
  1. Traffic log report (csv + Counter)
  2. File integrity check (hashlib + SQLite history)
  3. Port check (socket)
  4. External API demo (requests)
"""

from __future__ import annotations

import requests

from .logic import build_traffic_report, check_and_record_port, check_file_integrity, fetch_random_uuid
from .models import TriageDatabase
from .utils import prompt_int, validate_non_empty, validate_port

MENU_TEXT = """
==================================
   Security Triage Toolkit
==================================
1. Analyze a traffic log (top talkers, top ports, flagged ports)
2. Check a file's integrity (hash + compare to history)
3. Check if a host:port is open
4. Fetch a demo UUID from an external API
5. Show recent port-check history
0. Exit
"""


def run_traffic_report() -> None:
    """Prompt for a CSV path and print a traffic summary report."""
    path = validate_non_empty(input("Path to traffic CSV [data/sample_data.csv]: ") or "data/sample_data.csv")
    try:
        report = build_traffic_report(path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return

    print(f"\nTotal connections parsed: {report['total_connections']}")

    print("\nTop talkers by bytes:")
    if not report["top_talkers"]:
        print("  (no data)")
    for ip, total_bytes in report["top_talkers"]:
        print(f"  {ip:<15} {total_bytes:>8} bytes")

    print("\nTop destination ports by connection count:")
    for port, count in report["top_ports"]:
        print(f"  port {port:<6} {count} connection(s)")

    print("\nFlagged (suspicious-port) connections:")
    if not report["flagged"]:
        print("  none")
    for conn in report["flagged"]:
        print(f"  SUSPICIOUS: {conn.timestamp} {conn.src_ip} -> port {conn.dst_port} ({conn.protocol})")


def run_file_integrity_check(db: TriageDatabase) -> None:
    """Prompt for a file path, hash it, and report match/mismatch/first-seen."""
    path = validate_non_empty(input("Path to file to check: "))
    try:
        result = check_file_integrity(path, db)
    except FileNotFoundError:
        print(f"Error: file not found: '{path}'")
        return
    except PermissionError:
        print(f"Error: permission denied reading '{path}'")
        return

    if result["status"] == "first_seen":
        print(f"First time seeing this file. Recorded sha256: {result['sha256']}")
    elif result["status"] == "match":
        print(f"OK — hash matches previous record. sha256: {result['sha256']}")
    else:
        print("MISMATCH — file has changed since it was last recorded!")
        print(f"  current:  {result['sha256']}")
        print(f"  previous: {result['previous_sha256']} (recorded {result['previous_recorded_at']})")


def run_port_check(db: TriageDatabase) -> None:
    """Prompt for host/port, run the check (local/authorized targets only)."""
    host = validate_non_empty(input("Host to check [127.0.0.1]: ") or "127.0.0.1")
    raw_port = input("Port to check [22]: ") or "22"
    try:
        port = validate_port(raw_port)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    try:
        result = check_and_record_port(host, port, db)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    print(f"{result.host}:{result.port} -> {result.status}")


def run_api_demo() -> None:
    """Fetch and print a demo UUID, handling network errors gracefully."""
    try:
        uuid_value = fetch_random_uuid()
        print(f"Fetched UUID: {uuid_value}")
    except requests.RequestException as exc:
        print(f"Error: could not reach the API ({exc}).")


def run_history(db: TriageDatabase) -> None:
    """Print the most recent port checks stored in the database."""
    rows = db.recent_port_checks(limit=10)
    if not rows:
        print("No port checks recorded yet.")
        return
    print("\nRecent port checks:")
    for row in rows:
        print(f"  {row['checked_at']}  {row['host']}:{row['port']} -> {row['status']}")


def main() -> None:
    """Run the interactive menu loop until the user chooses to exit."""
    with TriageDatabase("data/triage.db") as db:
        while True:
            print(MENU_TEXT)
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    run_traffic_report()
                elif choice == "2":
                    run_file_integrity_check(db)
                elif choice == "3":
                    run_port_check(db)
                elif choice == "4":
                    run_api_demo()
                elif choice == "5":
                    run_history(db)
                elif choice == "0":
                    print("Goodbye.")
                    break
                else:
                    print(f"'{choice}' isn't a valid option — pick a number from the menu.")
            except ValueError as exc:
                # Catches validation errors that slipped through, so a bad
                # input never crashes the whole session.
                print(f"Error: {exc}")


if __name__ == "__main__":
    main()
