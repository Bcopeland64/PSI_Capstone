import os
import sys

import pandas as pd


# Add the src folder so we can import project files
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from utils import validate_ip, validate_port
from logic import SecurityTriage


def test_valid_ip():
    """Test a valid IP address."""
    assert validate_ip("192.168.1.10") is True


def test_invalid_ip():
    """Test an invalid IP address."""
    assert validate_ip("999.999.999.999") is False


def test_valid_port():
    """Test a valid port number."""
    assert validate_port(443) is True


def test_invalid_port():
    """Test an invalid port number."""
    assert validate_port(70000) is False


def test_load_data(tmp_path):
    """Test loading security log data from a CSV file."""
    test_file = tmp_path / "test_logs.csv"

    test_data = pd.DataFrame({
        "timestamp": ["2026-09-19 10:00:00"],
        "src_ip": ["192.168.1.10"],
        "dst_ip": ["10.0.0.5"],
        "dst_port": [443],
        "protocol": ["TCP"],
        "bytes": [1000],
        "status": ["success"]
    })

    test_data.to_csv(test_file, index=False)

    triage = SecurityTriage(test_file)

    result = triage.load_data()

    assert result is True
    assert triage.data is not None
    assert len(triage.data) == 1


def test_failed_logins(tmp_path):
    """Test detection of failed login events."""
    test_file = tmp_path / "test_logs.csv"

    test_data = pd.DataFrame({
        "timestamp": [
            "2026-09-19 10:00:00",
            "2026-09-19 10:01:00"
        ],
        "src_ip": [
            "192.168.1.10",
            "10.0.0.8"
        ],
        "dst_ip": [
            "10.0.0.5",
            "10.0.0.5"
        ],
        "dst_port": [
            443,
            22
        ],
        "protocol": [
            "TCP",
            "TCP"
        ],
        "bytes": [
            1000,
            150
        ],
        "status": [
            "success",
            "failed"
        ]
    })

    test_data.to_csv(test_file, index=False)

    triage = SecurityTriage(test_file)

    triage.load_data()
    triage.clean_data()

    failed_logins = triage.find_failed_logins()

    assert len(failed_logins) == 1
    assert failed_logins.iloc[0]["status"] == "failed"
    