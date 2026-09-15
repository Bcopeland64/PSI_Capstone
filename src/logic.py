"""
logic.py
--------
Business/data-processing layer. Contains the TriageEngine, which turns
a ticket's raw text and category into a priority score and level, plus
pure functions that compute summary statistics over a list of tickets.

Keeping this separate from database.py means the scoring rules can be
changed or unit tested without touching SQLite at all.
"""

from collections import Counter

from src.models import Category, Priority, Ticket

# Keywords that bump up a ticket's urgency score. Weight is added once
# per keyword found (case-insensitive) in the title + description.
_URGENT_KEYWORDS = {
    "down": 25,
    "outage": 30,
    "crash": 20,
    "data loss": 35,
    "breach": 40,
    "security": 25,
    "urgent": 20,
    "cannot login": 15,
    "can't login": 15,
    "payment failed": 20,
    "blocked": 10,
}

# Baseline score contributed just by category, before keyword scanning.
_CATEGORY_BASE_SCORE = {
    Category.SECURITY: 40,
    Category.OUTAGE: 35,
    Category.BILLING: 15,
    Category.BUG: 10,
    Category.FEATURE_REQUEST: 0,
    Category.OTHER: 5,
}


class TriageEngine:
    """
    Encapsulates the rules for turning ticket content into a priority.

    Score is 0-100. Thresholds map the score onto a Priority level.
    Everything is a pure computation with no side effects, so it is
    easy to test in isolation (see tests/test_logic.py).
    """

    def __init__(self, thresholds: dict[str, int] | None = None):
        # Minimum score required to reach each priority level.
        self.thresholds = thresholds or {
            "CRITICAL": 60,
            "HIGH": 35,
            "MEDIUM": 15,
            "LOW": 0,
        }

    def score(self, ticket: Ticket) -> int:
        """Compute a 0-100 urgency score for a ticket."""
        text = f"{ticket.title} {ticket.description}".lower()
        total = _CATEGORY_BASE_SCORE.get(ticket.category, 5)
        for keyword, weight in _URGENT_KEYWORDS.items():
            if keyword in text:
                total += weight
        return max(0, min(total, 100))

    def classify(self, score: int) -> Priority:
        """Map a numeric score onto a Priority level using thresholds."""
        if score >= self.thresholds["CRITICAL"]:
            return Priority.CRITICAL
        if score >= self.thresholds["HIGH"]:
            return Priority.HIGH
        if score >= self.thresholds["MEDIUM"]:
            return Priority.MEDIUM
        return Priority.LOW

    def triage(self, ticket: Ticket) -> Ticket:
        """Score a ticket and set its priority/priority_score in place."""
        ticket.priority_score = self.score(ticket)
        ticket.priority = self.classify(ticket.priority_score)
        return ticket


def summarize(tickets: list[Ticket]) -> dict:
    """
    Compute aggregate statistics for a collection of tickets.

    Returns a dict with counts by status, counts by priority, counts
    by category, and the average priority score. Safe to call with an
    empty list (returns zeroed-out structures rather than raising).
    """
    if not tickets:
        return {
            "total": 0,
            "by_status": {},
            "by_priority": {},
            "by_category": {},
            "avg_score": 0.0,
        }

    by_status = Counter(t.status.value for t in tickets)
    by_priority = Counter(t.priority.value for t in tickets)
    by_category = Counter(t.category.value for t in tickets)
    avg_score = sum(t.priority_score for t in tickets) / len(tickets)

    return {
        "total": len(tickets),
        "by_status": dict(by_status),
        "by_priority": dict(by_priority),
        "by_category": dict(by_category),
        "avg_score": round(avg_score, 1),
    }


def sort_by_urgency(tickets: list[Ticket]) -> list[Ticket]:
    """Return tickets ordered most-urgent first (priority rank, then score)."""
    return sorted(tickets, key=lambda t: (t.priority.rank, t.priority_score), reverse=True)
