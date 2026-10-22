"""Unit tests for the triage engine."""

from datetime import datetime

import pytest

from src.logic import TriageEngine
from src.models import Incident


@pytest.fixture
def engine() -> TriageEngine:
    """Return a triage engine for tests."""
    return TriageEngine()


def make_incident(attack_type: str) -> Incident:
    """Create a valid test incident."""
    return Incident(
        incident_id="TEST001",
        timestamp=datetime(2026, 9, 20, 10, 0, 0),
        source_ip="192.168.1.10",
        destination_ip="10.0.0.5",
        attack_type=attack_type,
        username="testuser",
        description="Test incident",
    )


def test_malware_is_critical(engine: TriageEngine) -> None:
    """Malware should produce CRITICAL severity."""
    incident = make_incident("Malware")
    assert engine.calculate_score(incident.attack_type) == 5
    assert engine.score_to_severity(5) == "CRITICAL"


def test_sql_injection_is_high(engine: TriageEngine) -> None:
    """SQL injection should produce HIGH severity."""
    incident = make_incident("SQL Injection")
    assert engine.calculate_score(incident.attack_type) == 4
    assert engine.score_to_severity(4) == "HIGH"


def test_phishing_is_medium(engine: TriageEngine) -> None:
    """Phishing should produce MEDIUM severity."""
    incident = make_incident("Phishing")
    assert engine.calculate_score(incident.attack_type) == 3
    assert engine.score_to_severity(3) == "MEDIUM"


def test_port_scan_is_low(engine: TriageEngine) -> None:
    """Port scan should produce LOW severity."""
    incident = make_incident("Port Scan")
    assert engine.calculate_score(incident.attack_type) == 1
    assert engine.score_to_severity(1) == "LOW"


def test_invalid_source_ip_is_rejected(
    engine: TriageEngine,
) -> None:
    """An invalid source IP should raise ValueError."""
    row = {
        "incident_id": "TEST002",
        "timestamp": "2026-09-20 10:00:00",
        "source_ip": "not-an-ip",
        "destination_ip": "10.0.0.5",
        "attack_type": "Malware",
        "username": "admin",
        "description": "Invalid IP test",
    }

    with pytest.raises(ValueError, match="Invalid source IP"):
        engine.create_incident(row)


def test_invalid_timestamp_is_rejected(
    engine: TriageEngine,
) -> None:
    """An invalid timestamp should raise ValueError."""
    row = {
        "incident_id": "TEST003",
        "timestamp": "20-09-2026",
        "source_ip": "192.168.1.10",
        "destination_ip": "10.0.0.5",
        "attack_type": "Port Scan",
        "username": "user",
        "description": "Invalid timestamp test",
    }

    with pytest.raises(ValueError, match="Invalid timestamp"):
        engine.create_incident(row)


def test_unknown_attack_defaults_to_low(
    engine: TriageEngine,
) -> None:
    """Unknown attack types should receive the default LOW score."""
    assert engine.calculate_score("Unknown") == 1
    assert engine.score_to_severity(1) == "LOW"
