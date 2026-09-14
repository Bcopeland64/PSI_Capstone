class Incident:
    """
    Represents a cybersecurity incident.
    """

    def __init__(self, incident_id, title, severity, status):
        self.incident_id = incident_id
        self.title = title
        self.severity = severity
        self.status = status

    def to_dict(self):
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["incident_id"],
            data["title"],
            data["severity"],
            data["status"]
        )