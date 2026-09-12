"""Unit tests for src/logic.py.

Run with:  pytest  (from the capstone_project/ root)

Uses pytest's tmp_path fixture so tests never touch real project files —
each test gets its own throwaway directory.
"""

import sys
from pathlib import Path

# Allow `import src...` when pytest is run from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.logic import (
    build_traffic_report,
    check_file_integrity,
    flag_suspicious_ports,
    load_connections,
    port_connection_counts,
    top_talkers_by_bytes,
)
from src.models import TriageDatabase

SAMPLE_CSV = """timestamp,src_ip,dst_port,protocol,bytes
2026-03-02T11:00:01,10.2.0.5,443,tcp,4000
2026-03-02T11:00:04,10.2.0.6,53,udp,120
2026-03-02T11:00:09,10.2.0.5,443,tcp,6500
2026-03-02T11:00:12,10.2.0.9,4444,tcp,50
2026-03-02T11:00:30,10.2.0.5,443,tcp,2200
"""


def make_csv(tmp_path: Path) -> str:
    csv_path = tmp_path / "traffic.csv"
    csv_path.write_text(SAMPLE_CSV)
    return str(csv_path)


def test_load_connections_parses_all_rows(tmp_path):
    connections = load_connections(make_csv(tmp_path))
    assert len(connections) == 5
    assert connections[0].src_ip == "10.2.0.5"
    assert connections[0].num_bytes == 4000


def test_load_connections_missing_file_raises(tmp_path):
    missing = tmp_path / "does_not_exist.csv"
    try:
        load_connections(str(missing))
        assert False, "expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_top_talkers_by_bytes_ranks_correctly(tmp_path):
    connections = load_connections(make_csv(tmp_path))
    result = top_talkers_by_bytes(connections, top_n=1)
    assert result[0][0] == "10.2.0.5"
    assert result[0][1] == 4000 + 6500 + 2200


def test_port_connection_counts(tmp_path):
    connections = load_connections(make_csv(tmp_path))
    counts = dict(port_connection_counts(connections))
    assert counts[443] == 3
    assert counts[53] == 1


def test_flag_suspicious_ports_finds_watchlist_hit(tmp_path):
    connections = load_connections(make_csv(tmp_path))
    flagged = flag_suspicious_ports(connections)
    assert len(flagged) == 1
    assert flagged[0].dst_port == 4444


def test_build_traffic_report_shape(tmp_path):
    report = build_traffic_report(make_csv(tmp_path))
    assert report["total_connections"] == 5
    assert "top_talkers" in report and "top_ports" in report


def test_check_file_integrity_first_seen_then_match(tmp_path):
    target = tmp_path / "note.txt"
    target.write_text("hello world\n")
    db_path = tmp_path / "triage.db"

    with TriageDatabase(str(db_path)) as db:
        first = check_file_integrity(str(target), db)
        assert first["status"] == "first_seen"

        second = check_file_integrity(str(target), db)
        assert second["status"] == "match"
        assert second["sha256"] == first["sha256"]


def test_check_file_integrity_detects_mismatch(tmp_path):
    target = tmp_path / "note.txt"
    target.write_text("original content\n")
    db_path = tmp_path / "triage.db"

    with TriageDatabase(str(db_path)) as db:
        check_file_integrity(str(target), db)  # first_seen
        target.write_text("changed content\n")
        result = check_file_integrity(str(target), db)
        assert result["status"] == "mismatch"
