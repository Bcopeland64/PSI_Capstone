class Incident:
    """Represents a cybersecurity incident."""

    def __init__(self, incident_id, incident_type, description, severity):
        self.incident_id = incident_id
        self.incident_type = incident_type
        self.description = description
        self.severity = severity
        self.status = "Open"

    def to_dict(self):
        """Convert the incident to a dictionary."""
        return {
            "id": self.incident_id,
            "type": self.incident_type,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
        }