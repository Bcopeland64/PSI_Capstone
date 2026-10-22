"""Tests for SQLite persistence."""

from datetime import datetime

from src.data_handler import DataHandler
from src.models import Incident


def test_save_and_search_incident(tmp_path) -> None:
    """An incident can be saved and retrieved from SQLite."""
    database = tmp_path / "test.db"
    handler = DataHandler(str(database))
    handler.initialize_database()

    incident = Incident(
        incident_id="DB001",
        timestamp=datetime(2026, 9, 20, 10, 0, 0),
        source_ip="192.168.1.10",
        destination_ip="10.0.0.5",
        attack_type="Port Scan",
        username="tester",
        description="Database persistence test",
        severity="LOW",
        score=1,
    )

    assert handler.save_incidents([incident]) == 1

    result = handler.search_incident("DB001")

    assert result is not None
    assert result[0] == "DB001"
    assert result[7] == "LOW"
    assert result[8] == 1
