from src.risk import calculate_risk_score


def test_low_risk():
    """Test analysis containing no suspicious events."""

    analysis = {
        "events": {
            "failed_login": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
            "denied": 0,
        },
        "ip_counts": {},
    }

    score, level, reasons = calculate_risk_score(analysis)

    assert score == 0
    assert level == "LOW"
    assert reasons == []


def test_critical_risk():
    """Test analysis containing serious security events."""

    analysis = {
        "events": {
            "failed_login": 3,
            "warning": 0,
            "error": 0,
            "critical": 1,
            "denied": 0,
        },
        "ip_counts": {
            "45.33.12.9": 3,
        },
    }

    score, level, reasons = calculate_risk_score(analysis)

    assert score == 12
    assert level == "CRITICAL"
    assert len(reasons) > 0