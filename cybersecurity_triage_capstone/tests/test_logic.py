"""Unit tests for triage logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import TriageCase
from logic import calculate_risk, get_recommendation, search_cases


def make_case(**kwargs):
    defaults = {
        "case_id": "1",
        "file_name": "test.exe",
        "file_size": 100,
        "executable": False,
        "downloaded": False,
        "antivirus_triggered": False,
        "suspicious_extension": False,
        "notes": "test",
    }
    defaults.update(kwargs)
    return TriageCase(**defaults)


def test_high_risk_case():
    case = make_case(
        executable=True,
        downloaded=True,
        antivirus_triggered=True,
        suspicious_extension=True,
    )
    calculate_risk(case)
    assert case.risk_score == 10
    assert case.risk_level == "HIGH"


def test_low_risk_case():
    case = make_case()
    calculate_risk(case)
    assert case.risk_score == 0
    assert case.risk_level == "LOW"


def test_recommendation():
    assert "Isolate" in get_recommendation("HIGH")


def test_search():
    cases = [make_case(file_name="malware.exe")]
    results = search_cases(cases, "malware")
    assert len(results) == 1
