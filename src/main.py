"""
main.py
-------
Entry point for the Security Alert Triage CLI.
Run with: python -m src.main
"""

from src.logic import load_alerts, classify_all, summarize_by_source, export_report

DEFAULT_INPUT_PATH = "data/sample_alerts.csv"
DEFAULT_OUTPUT_PATH = "data/report.json"


def print_menu():
    print("\nWhat would you like to do?")
    print("  1. Load and triage alerts")
    print("  2. View summary by source IP")
    print("  3. Export report to JSON")
    print("  4. Exit")


def run():
    alerts = None       # nothing loaded yet
    summaries = None    # nothing summarized yet

    while True:
        print_menu()
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            try:
                alerts = load_alerts(DEFAULT_INPUT_PATH)
                classify_all(alerts)
            except FileNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "2":
            if alerts is None:
                print("Load alerts first (option 1).")
                continue
            summaries = summarize_by_source(alerts)
            for s in summaries:
                print(f"{s['source_ip']:<16} {s['highest_severity']:<10} "
                      f"attempts={s['total_failed_attempts']} events={s['event_types']}")

        elif choice == "3":
            if alerts is None:
                print("Load alerts first (option 1).")
                continue
            if summaries is None:
                summaries = summarize_by_source(alerts)
            export_report(summaries, DEFAULT_OUTPUT_PATH)

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Please choose a number between 1 and 4.")


if __name__ == "__main__":
    run()