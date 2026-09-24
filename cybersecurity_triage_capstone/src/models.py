"""Data models for the Cybersecurity Triage Tool."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict


@dataclass
class TriageCase:
    """Represents a cybersecurity triage case."""

    case_id: str
    file_name: str
    file_size: int
    executable: bool
    downloaded: bool
    antivirus_triggered: bool
    suspicious_extension: bool
    notes: str
    risk_score: int = 0
    risk_level: str = "LOW"
    created_at: str = ""

    def to_dict(self) -> Dict:
        """Convert the case to a dictionary for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        """Create a TriageCase from stored dictionary data."""
        return cls(**data)

    def set_created_at(self) -> None:
        """Set creation time if it has not already been set."""
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
