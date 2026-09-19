import os

from logic import SecurityTriage


def show_menu():
    """Display the main menu."""
    print("\n==============================")
    print("   SECURITY LOG TRIAGE TOOL")
    print("==============================")
    print("1. Load Security Logs")
    print("2. Clean Data")
    print("3. Show Failed Logins")
    print("4. Show Sensitive Port Activity")
    print("5. Show Top Source IPs")
    print("6. Show Summary")
    print("7. Generate Report")
    print("8. Exit")


def main():
    """Run the Security Log Triage application."""

    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    input_file = os.path.join(
        project_dir,
        "data",
        "security_logs.csv"
    )

    output_file = os.path.join(
        project_dir,
        "data",
        "triage_report.csv"
    )

    triage = SecurityTriage(input_file)

    while True:
        show_menu()

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            triage.load_data()

        elif choice == "2":
            triage.clean_data()

        elif choice == "3":
            failed_logins = triage.find_failed_logins()

            if failed_logins is not None:
                if failed_logins.empty:
                    print("No failed login events found.")
                else:
                    print("\nFailed Login Events:")
                    print(failed_logins.to_string(index=False))

        elif choice == "4":
            sensitive_events = triage.find_sensitive_ports()

            if sensitive_events is not None:
                if sensitive_events.empty:
                    print("No sensitive port activity found.")
                else:
                    print("\nSensitive Port Activity:")
                    print(sensitive_events.to_string(index=False))

        elif choice == "5":
            top_ips = triage.top_source_ips()

            if top_ips is not None:
                print("\nTop Source IP Addresses:")
                print(top_ips)

        elif choice == "6":
            summary = triage.get_summary()

            if summary is not None:
                print("\n===== TRIAGE SUMMARY =====")
                print("Total Events:", summary["total_events"])
                print("Failed Logins:", summary["failed_logins"])
                print(
                    "Sensitive Port Events:",
                    summary["sensitive_port_events"]
                )
                print(
                    "Unique Source IPs:",
                    summary["unique_source_ips"]
                )

        elif choice == "7":
            triage.generate_report(output_file)

        elif choice == "8":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
    