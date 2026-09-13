"""
test_logic.py
-------------
Tests for the triage classification rules.
Run with: pytest tests/ -v
"""

from src.models import make_alert, classify_alert


def test_successful_login_is_low():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "dina", "successful login", 0)
    assert classify_alert(alert) == "LOW"


def test_few_failed_attempts_is_medium():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "dina", "failed login", 3)
    assert classify_alert(alert) == "MEDIUM"


def test_many_failed_attempts_is_high():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "dina", "failed login", 7)
    assert classify_alert(alert) == "HIGH"


def test_extreme_failed_attempts_is_critical():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "dina", "failed login", 15)
    assert classify_alert(alert) == "CRITICAL"


def test_single_root_login_attempt_is_high():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "root", "root login attempt", 1)
    assert classify_alert(alert) == "HIGH"


def test_repeated_root_login_attempts_is_critical():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "root", "root login attempt", 2)
    assert classify_alert(alert) == "CRITICAL"


def test_privilege_escalation_is_always_critical():
    alert = make_alert("2026-09-01 12:00:00", "192.168.1.1", "root", "privilege escalation", 0)
    assert classify_alert(alert) == "CRITICAL"