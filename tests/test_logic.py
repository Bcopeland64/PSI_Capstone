from src.logic import calculate_priority, count_by_severity


def test_critical_priority():
    assert calculate_priority("Critical") == "Critical"


def test_high_priority():
    assert calculate_priority("High") == "High"


def test_medium_priority():
    assert calculate_priority("Medium") == "Medium"


def test_low_priority():
    assert calculate_priority("Low") == "Low"


def test_count_by_severity():
    incidents = [
        {"severity": "High"},
        {"severity": "Low"},
        {"severity": "High"},
    ]

    result = count_by_severity(incidents)

    assert result["High"] == 2
    assert result["Low"] == 1