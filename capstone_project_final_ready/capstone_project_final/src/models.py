"""Data models used by the security triage application."""

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class LogEvent:
    """Represent a single authentication log event."""

    timestamp: str
    host: str
    username: Optional[str]
    source_ip: Optional[str]
    status: str
    raw_message: str

    def to_dict(self) -> dict:
        """Convert the event to a dictionary."""
        return asdict(self)


@dataclass
class TriageResult:
    """Represent the final triage analysis."""

    total_events: int
    failed_logins: int
    successful_logins: int
    other_events: int
    unique_ips: int
    suspicious_ips: dict
    suspicious_event_count: int

    def to_dict(self) -> dict:
        """Convert the result to a dictionary."""
        return asdict(self)
