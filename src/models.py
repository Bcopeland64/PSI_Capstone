"""Data models used by the security incident triage application."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Incident:
    """Represent a security incident."""

    incident_id: str
    timestamp: datetime
    source_ip: str
    destination_ip: str
    attack_type: str
    username: str
    description: str
    severity: str = "UNKNOWN"
    score: int = 0

    def set_triage_result(self, severity: str, score: int) -> None:
        """Store the triage result for the incident."""
        self.severity = severity
        self.score = score

    def to_dict(self) -> dict:
        """Return a serializable dictionary representation."""
        return {
            "incident_id": self.incident_id,
            "timestamp": self.timestamp.isoformat(sep=" "),
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "attack_type": self.attack_type,
            "username": self.username,
            "description": self.description,
            "severity": self.severity,
            "score": self.score,
        }
