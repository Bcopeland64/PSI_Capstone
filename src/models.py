"""
models.py
---------
Core domain objects for the Support Ticket Triage System.

Defines the Ticket entity plus the enumerations that constrain its
valid states. Keeping these in one module means every other part of
the application (persistence, business logic, CLI) shares a single
source of truth for what a "ticket" is.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    """Lifecycle states a ticket can be in."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

    @classmethod
    def values(cls) -> list[str]:
        return [status.value for status in cls]


class Priority(str, Enum):
    """Triage priority levels, ordered from least to most urgent."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def rank(self) -> int:
        """Numeric rank so priorities can be sorted/compared."""
        order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        return order[self.value]

    @classmethod
    def values(cls) -> list[str]:
        return [priority.value for priority in cls]


class Category(str, Enum):
    """Broad classification of the reported issue."""

    BUG = "BUG"
    OUTAGE = "OUTAGE"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    SECURITY = "SECURITY"
    BILLING = "BILLING"
    OTHER = "OTHER"

    @classmethod
    def values(cls) -> list[str]:
        return [category.value for category in cls]


@dataclass
class Ticket:
    """
    Represents a single support ticket.

    `ticket_id` is None for a ticket that has not yet been persisted;
    the data layer assigns the real id once it is inserted into storage.
    """

    title: str
    description: str
    category: Category
    reporter: str
    priority: Priority = Priority.MEDIUM
    status: Status = Status.OPEN
    priority_score: int = 0
    ticket_id: int | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def touch(self) -> None:
        """Refresh the `updated_at` timestamp. Call after any mutation."""
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def as_dict(self) -> dict:
        """Serialize to a plain dict (enums become their string values)."""
        return {
            "ticket_id": self.ticket_id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value if isinstance(self.category, Category) else self.category,
            "reporter": self.reporter,
            "priority": self.priority.value if isinstance(self.priority, Priority) else self.priority,
            "status": self.status.value if isinstance(self.status, Status) else self.status,
            "priority_score": self.priority_score,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_row(row: dict) -> "Ticket":
        """Reconstruct a Ticket from a database row / dict-like object."""
        return Ticket(
            ticket_id=row["ticket_id"],
            title=row["title"],
            description=row["description"],
            category=Category(row["category"]),
            reporter=row["reporter"],
            priority=Priority(row["priority"]),
            status=Status(row["status"]),
            priority_score=row["priority_score"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
