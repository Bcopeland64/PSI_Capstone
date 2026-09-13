"""
test_logic.py
--------------
Unit tests for TriageEngine and Ticket, plus a couple of repository/CSV
round-trip checks. Run with:  pytest
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from src.data_handler import TicketRepository, export_csv, import_csv
from src.logic import TriageEngine
from src.models import Ticket
from src.utils import ValidationError, require_int_in_range, require_non_empty


@pytest.fixture
def engine():
    return TriageEngine()


def test_classify_severity_critical(engine):
    assert engine.classify_severity("Production server is down, total outage") == "critical"


def test_classify_severity_low_fallback(engine):
    # No keywords match at all -> should fall back to "low", not crash.
    assert engine.classify_severity("Just saying hello") == "low"


def test_classify_team_billing(engine):
    assert engine.classify_team("My invoice charge was wrong") == "billing"


def test_classify_team_fallback_support(engine):
    assert engine.classify_team("blah blah nothing matches") == "support"


def test_triage_sets_due_date(engine):
    ticket = Ticket(title="Server outage", description="Server is down", reporter="Test")
    engine.triage(ticket)
    assert ticket.severity == "critical"
    assert ticket.due_at is not None


def test_ticket_status_transition_valid():
    ticket = Ticket(title="t", description="d", reporter="r")
    ticket.mark_status("in_progress")
    assert ticket.status == "in_progress"


def test_ticket_status_transition_invalid():
    ticket = Ticket(title="t", description="d", reporter="r")
    with pytest.raises(ValueError):
        ticket.mark_status("not_a_real_status")


def test_summarize_counts(engine):
    tickets = [
        engine.triage(Ticket(title="Server down", description="outage", reporter="a")),
        engine.triage(Ticket(title="Typo", description="cosmetic typo", reporter="b")),
    ]
    summary = TriageEngine.summarize(tickets)
    assert summary["total"] == 2
    assert "critical" in summary["by_severity"] or "low" in summary["by_severity"]


def test_require_non_empty_raises_on_blank():
    with pytest.raises(ValidationError):
        require_non_empty("   ", "Title")


def test_require_int_in_range_valid():
    assert require_int_in_range("5", "Priority", 1, 10) == 5


def test_require_int_in_range_invalid():
    with pytest.raises(ValidationError):
        require_int_in_range("999", "Priority", 1, 10)


def test_repository_add_and_get(tmp_path):
    db_path = tmp_path / "test.db"
    repo = TicketRepository(db_path=str(db_path))
    ticket = Ticket(title="t", description="d", reporter="r")
    repo.add(ticket)
    assert ticket.ticket_id is not None
    fetched = repo.get(ticket.ticket_id)
    assert fetched.title == "t"
    repo.close()


def test_csv_round_trip(tmp_path):
    tickets = [Ticket(title="a", description="b", reporter="c")]
    csv_path = tmp_path / "out.csv"
    export_csv(tickets, str(csv_path))
    loaded = import_csv(str(csv_path))
    assert len(loaded) == 1
    assert loaded[0].title == "a"


def test_import_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        import_csv("does_not_exist.csv")
