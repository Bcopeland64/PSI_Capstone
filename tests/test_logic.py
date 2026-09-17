import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from logic import sort_by_severity
from models import Alert


def test_sort_by_severity_highest_first():
    alerts = [
        Alert("A1", "Port Scan", "Low", "10.0.0.1"),
        Alert("A2", "Ransomware", "Critical", "10.0.0.2"),
    ]
    result = sort_by_severity(alerts)
    assert result[0].alert_id == "A2"
