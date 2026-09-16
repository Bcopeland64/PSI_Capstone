"""Domain models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """A single task in the inventory."""
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.id < 1:
            raise ValueError("ID must be a positive integer")

    def to_dict(self):
        """Return a JSON-serializable dict."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "done": self.done,
            "created_at": self.created_at,
        }

    def mark_done(self):
        """Mark this task as completed."""
        self.done = True
