import json
import os

import requests

from models import Incident
from utils import validate_severity, get_non_empty_input
from logic import calculate_priority, count_by_severity


DATA_FILE = "data/incidents.json"


def load_incidents():
    """Load incidents from the JSON file."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("The data file is invalid. Starting with empty data.")
        return []


def save_incidents(incidents):
    """Save incidents to the JSON file."""
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(incidents, file, indent=4)


def add_incident(incidents):
    """Create and save a new cybersecurity incident."""
    print("\n--- Add New Incident ---")

    incident_type = get_non_empty_input("Enter incident type: ")
    description = get_non_empty_input("Enter description: ")

    while True:
        severity = input(
            "Enter severity (Low/Medium/High/Critical): "
        ).strip().title()

        if validate_severity(severity):
            break

        print("Invalid severity. Please choose Low, Medium, High, or Critical.")

    incident_id = len(incidents) + 1

    incident = Incident(
        incident_id,
        incident_type,
        description,
        severity,
    )

    incidents.append(incident.to_dict())
    save_incidents(incidents)

    priority = calculate_priority(severity)

    print("\nIncident added successfully!")
    print(f"Incident ID: {incident_id}")
    print(f"Priority: {priority}")


def view_incidents(incidents):
    """Display all saved incidents."""
    print("\n--- All Incidents ---")

    if not incidents:
        print("No incidents found.")
        return

    for incident in incidents:
        priority = calculate_priority(incident["severity"])

        print("\n-------------------------")
        print(f"ID: {incident['id']}")
        print(f"Type: {incident['type']}")
        print(f"Description: {incident['description']}")
        print(f"Severity: {incident['severity']}")
        print(f"Priority: {priority}")
        print(f"Status: {incident['status']}")


def show_summary(incidents):
    """Display a summary of incidents by severity."""
    print("\n--- Incident Summary ---")

    if not incidents:
        print("No incidents found.")
        return

    counts = count_by_severity(incidents)

    for severity, count in counts.items():
        print(f"{severity}: {count}")


def check_external_service():
    """Check an external service using an HTTP request."""
    print("\n--- External Service Check ---")

    try:
        response = requests.get(
            "https://httpbin.org/get",
            timeout=5,
        )

        if response.status_code == 200:
            print("External service is reachable.")
        else:
            print(
                f"External service returned status code "
                f"{response.status_code}."
            )

    except requests.RequestException:
        print("Could not connect to the external service.")


def main():
    """Run the Cybersecurity Incident Triage Tool."""
    incidents = load_incidents()

    while True:
        print("\n================================")
        print(" Cybersecurity Incident Triage")
        print("================================")
        print("1. Add Incident")
        print("2. View Incidents")
        print("3. Show Summary")
        print("4. Check External Service")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_incident(incidents)

        elif choice == "2":
            view_incidents(incidents)

        elif choice == "3":
            show_summary(incidents)

        elif choice == "4":
            check_external_service()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()