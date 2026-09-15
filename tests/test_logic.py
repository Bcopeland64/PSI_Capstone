"""
test_logic.py
-------------
Unit tests for the pure business logic (TriageEngine, summarize,
sort_by_urgency) and the input-validation helpers in utils.py.

Run with:  pytest tests/
"""

import sys
from pathlib import Path

# Make `src` importable when running `pytest` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from src.logic import TriageEngine, sort_by_urgency, summarize
from src.models import Category, Priority, Status, Ticket
from src.utils import ValidationError, parse_category, parse_positive_int, require_non_empty


def make_ticket(title="Issue", description="", category=Category.BUG) -> Ticket:
    return Ticket(title=title, description=description, category=category, reporter="tester")


# ---- TriageEngine ---------------------------------------------------------

def test_security_keyword_yields_critical():
    engine = TriageEngine()
    ticket = make_ticket(
        title="Possible security breach",
        description="Unauthorized access detected in admin panel",
        category=Category.SECURITY,
    )
    engine.triage(ticket)
    assert ticket.priority == Priority.CRITICAL
    assert ticket.priority_score >= 60


def test_feature_request_defaults_low():
    engine = TriageEngine()
    ticket = make_ticket(
        title="Add dark mode",
        description="Would be nice to have a dark theme option",
        category=Category.FEATURE_REQUEST,
    )
    engine.triage(ticket)
    assert ticket.priority == Priority.LOW


def test_outage_keyword_raises_priority():
    engine = TriageEngine()
    ticket = make_ticket(
        title="Service down",
        description="The API has been down for 10 minutes",
        category=Category.OUTAGE,
    )
    engine.triage(ticket)
    assert ticket.priority.rank >= Priority.HIGH.rank


def test_score_is_clamped_between_0_and_100():
    engine = TriageEngine()
    ticket = make_ticket(
        title="down outage crash breach security urgent blocked",
        description="data loss payment failed cannot login",
        category=Category.SECURITY,
    )
    engine.triage(ticket)
    assert 0 <= ticket.priority_score <= 100


# ---- summarize / sort_by_urgency ------------------------------------------

def test_summarize_empty_list():
    stats = summarize([])
    assert stats["total"] == 0
    assert stats["avg_score"] == 0.0


def test_summarize_counts_and_average():
    engine = TriageEngine()
    tickets = [
        make_ticket("A", "minor bug", Category.BUG),
        make_ticket("B", "security breach", Category.SECURITY),
    ]
    for t in tickets:
        engine.triage(t)
    stats = summarize(tickets)
    assert stats["total"] == 2
    assert set(stats["by_category"].keys()) == {"BUG", "SECURITY"}
    assert stats["avg_score"] == round((tickets[0].priority_score + tickets[1].priority_score) / 2, 1)


def test_sort_by_urgency_orders_descending():
    engine = TriageEngine()
    low = make_ticket("Low", "feature idea", Category.FEATURE_REQUEST)
    high = make_ticket("High", "outage crash", Category.OUTAGE)
    engine.triage(low)
    engine.triage(high)
    ordered = sort_by_urgency([low, high])
    assert ordered[0] is high
    assert ordered[1] is low


# ---- utils / validation -----------------------------------------------

def test_require_non_empty_rejects_blank():
    with pytest.raises(ValidationError):
        require_non_empty("   ", "Title")


def test_require_non_empty_strips_whitespace():
    assert require_non_empty("  hello  ", "Title") == "hello"


def test_parse_category_case_insensitive():
    assert parse_category("bug") == Category.BUG


def test_parse_category_invalid_raises():
    with pytest.raises(ValidationError):
        parse_category("not_a_category")


def test_parse_positive_int_rejects_non_numeric():
    with pytest.raises(ValidationError):
        parse_positive_int("abc", "Ticket ID")


def test_parse_positive_int_rejects_zero_or_negative():
    with pytest.raises(ValidationError):
        parse_positive_int("0", "Ticket ID")
    with pytest.raises(ValidationError):
        parse_positive_int("-5", "Ticket ID")


def test_parse_positive_int_accepts_valid():
    assert parse_positive_int("42", "Ticket ID") == 42
