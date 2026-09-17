"""
models.py
Defines data structures and classes for the security triage project.
"""

from datetime import datetime


class Incident:
    """Base class representing a general security incident."""

    def __init__(self, incident_id: str, title: str, severity: str, timestamp: str = None):
        self.incident_id = incident_id
        self.title = title
        self.severity = severity.upper()
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Converts object attributes to a dictionary for persistence."""
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "type": "General"
        }

    def __str__(self) -> str:
        return f"[{self.severity}] ID: {self.incident_id} | {self.title} ({self.timestamp})"


class NetworkIncident(Incident):
    """Subclass representing a network-specific security incident (Inheritance)."""

    def __init__(self, incident_id: str, title: str, severity: str, ip_address: str, timestamp: str = None):
        super().__init__(incident_id, title, severity, timestamp)
        self.ip_address = ip_address

    def to_dict(self) -> dict:
        """Extends parent dictionary conversion with network details."""
        data = super().to_dict()
        data["type"] = "Network"
        data["ip_address"] = self.ip_address
        return data

    def __str__(self) -> str:
        return f"[NETWORK] [{self.severity}] ID: {self.incident_id} | Target IP: {self.ip_address} | {self.title}"