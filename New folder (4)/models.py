"""Expense data models built using Object-Oriented Programming (OOP)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class Expense:
    """Represents an individual expense entry."""

    expense_id: str
    title: str
    amount: float
    category: str
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the Expense object into a dictionary for JSON storage."""
        return {
            "expense_id": self.expense_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Instantiates an Expense object from a dictionary."""
        return cls(
            expense_id=data["expense_id"],
            title=data["title"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
        )