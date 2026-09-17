"""
main.py
Main entry point for the Automated Incident Triage CLI tool.
"""

import sys
from models import Incident, NetworkIncident
from data_handler import DataHandler
from utils import validate_severity, validate_ip, get_valid_input


class TriageApp:
    """Main application controller class."""

    def __init__(self):
        self.data_handler = DataHandler()
        self.incidents = self.data_handler.load_incidents()

    def add_incident(self):
        """Workflow to collect inputs and store a new incident."""
        print("\n--- Add New Security Incident ---")
        inc_id = f"INC-{len(self.incidents) + 101}"
        title = input("Enter Incident Title: ").strip()

        severity = get_valid_input(
            "Enter Severity (LOW, MEDIUM, HIGH, CRITICAL): ",
            validate_severity,
            "Invalid severity level. Please try again."
        )

        is_network = input("Is this a network incident? (y/n): ").strip().lower()

        if is_network == 'y':
            ip_addr = get_valid_input(
                "Enter IP Address: ",
                validate_ip,
                "Invalid IP address format. (e.g., 192.168.1.1)"
            )
            obj = NetworkIncident(inc_id, title, severity, ip_address=ip_addr)
        else:
            obj = Incident(inc_id, title, severity)

        self.incidents.append(obj.to_dict())
        if self.data_handler.save_incidents(self.incidents):
            print(f"[Success] Incident added successfully: {obj}")

    def list_incidents(self):
        """Displays all recorded incidents."""
        print("\n--- Current Recorded Incidents ---")
        if not self.incidents:
            print("No incidents recorded yet.")
            return

        for idx, item in enumerate(self.incidents, 1):
            ip_info = f" | IP: {item.get('ip_address')}" if "ip_address" in item else ""
            print(f"{idx}. [{item['severity']}] {item['incident_id']} - {item['title']} (Type: {item['type']}){ip_info}")

    def run(self):
        """Main interaction loop."""
        while True:
            print("\n==================================")
            print("   AUTOMATED INCIDENT TRIAGE TOOL  ")
            print("==================================")
            print("1. Log New Incident")
            print("2. View All Incidents")
            print("3. Export Incidents Report (CSV)")
            print("4. Exit")

            choice = input("\nSelect an option (1-4): ").strip()

            if choice == "1":
                self.add_incident()
            elif choice == "2":
                self.list_incidents()
            elif choice == "3":
                self.data_handler.export_to_csv()
            elif choice == "4":
                print("\n[Exiting] Saving session state and closing application. Goodbye!")
                sys.exit(0)
            else:
                print("\n[Error] Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    app = TriageApp()
    app.run()