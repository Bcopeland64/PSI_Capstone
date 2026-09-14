from models import Incident
from data_handler import load_incidents, save_incidents


def add_incident():
    """
    Add a new incident.
    """

    incident_id = input("Enter Incident ID: ")
    title = input("Enter Incident Title: ")
    severity = input("Enter Severity (Low/Medium/High): ")

    incident = Incident(
        incident_id,
        title,
        severity,
        "Open"
    )

    incidents = load_incidents()
    incidents.append(incident.to_dict())
    save_incidents(incidents)

    print("Incident added successfully!")

def view_incidents():
    """
    Display all incidents.
    """

    incidents = load_incidents()

    if not incidents:
        print("No incidents found.")
        return

    print("\n=== Incident List ===")

    for incident in incidents:
        print(f"ID: {incident['incident_id']}")
        print(f"Title: {incident['title']}")
        print(f"Severity: {incident['severity']}")
        print(f"Status: {incident['status']}")
        print("-" * 30)   

def search_incident():
    """
    Search incident by ID.
    """

    incident_id = input("Enter Incident ID: ")

    incidents = load_incidents()

    for incident in incidents:
        if incident["incident_id"] == incident_id:
            print("\nIncident Found")
            print(f"ID: {incident['incident_id']}")
            print(f"Title: {incident['title']}")
            print(f"Severity: {incident['severity']}")
            print(f"Status: {incident['status']}")
            return

    print("Incident not found.")

def update_status():
    """
    Update incident status.
    """

    incident_id = input("Enter Incident ID: ")

    incidents = load_incidents()

    for incident in incidents:
        if incident["incident_id"] == incident_id:
            new_status = input("Enter New Status: ")

            incident["status"] = new_status

            save_incidents(incidents)

            print("Status updated successfully!")
            return

    print("Incident not found.")
    
def delete_incident():
    """
    Delete an incident.
    """

    incident_id = input("Enter Incident ID: ")

    incidents = load_incidents()

    for incident in incidents:
        if incident["incident_id"] == incident_id:

            incidents.remove(incident)

            save_incidents(incidents)

            print("Incident deleted successfully!")
            return

    print("Incident not found.")