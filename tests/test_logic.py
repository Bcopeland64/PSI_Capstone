import pytest
from src.utils import validate_ip
from src.models import SecurityAlert

def test_validate_ip_valid():
    """Test that valid IPv4 addresses return True."""
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("10.0.0.255") is True

def test_validate_ip_invalid():
    """Test that invalid IP formats or out-of-range values return False."""
    assert validate_ip("999.999.999.999") is False
    assert validate_ip("abc.def.ghi.jkl") is False
    assert validate_ip("192.168.1") is False

def test_security_alert_model():
    """Test SecurityAlert dictionary conversion and attributes mapping."""
    alert = SecurityAlert(
        ip_address="192.168.1.50",
        rule_name="Brute Force Detection",
        count=5,
        first_seen="2026-09-17 10:00:00",
        last_seen="2026-09-17 10:04:20",
        severity="High"
    )
    
    data = alert.to_dict()
    assert data["ip_address"] == "192.168.1.50"
    assert data["severity"] == "High"
    assert data["attempts"] == 5
    assert data["rule_name"] == "Brute Force Detection"