"""
test_logic.py
--------------
Unit tests for src/logic.py, src/utils.py, and src/models.py.

Run with:
    pytest tests/
from the project root (src/ must be importable, e.g. run from project root
so `src` resolves as a package).
"""

import os
import time

import pytest

from src.logic import (
    build_report,
    check_port,
    count_protocols,
    find_duplicates,
    find_top_talker,
    find_watchlist_hits,
    flag_recent_files,
    scan_folder,
    scan_port_range,
)
from src.models import Connection
from src.utils import (
    hash_file,
    human_bytes,
    validate_host,
    validate_port,
    validate_positive_int,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_connections():
    rows = [
        {"timestamp": "t1", "src_ip": "10.0.0.5", "dst_port": "443", "protocol": "tcp", "bytes": "500"},
        {"timestamp": "t2", "src_ip": "10.0.0.6", "dst_port": "53", "protocol": "udp", "bytes": "120"},
        {"timestamp": "t3", "src_ip": "10.0.0.5", "dst_port": "4444", "protocol": "tcp", "bytes": "9000"},
        {"timestamp": "t4", "src_ip": "10.0.0.7", "dst_port": "8080", "protocol": "tcp", "bytes": "300"},
    ]
    return [Connection.from_row(r) for r in rows]


@pytest.fixture
def evidence_folder(tmp_path):
    """Create a temp folder with two identical files and one unique file."""
    folder = tmp_path / "evidence"
    folder.mkdir()
    (folder / "a.txt").write_text("same content")
    (folder / "b.txt").write_text("same content")
    (folder / "c.txt").write_text("different content")

    old_file = folder / "old.txt"
    old_file.write_text("old")
    old_time = time.time() - 100000
    os.utime(old_file, (old_time, old_time))

    return str(folder)


# ---------------------------------------------------------------------------
# utils.py
# ---------------------------------------------------------------------------

def test_validate_positive_int_accepts_valid_value():
    assert validate_positive_int("5") == 5


def test_validate_positive_int_rejects_zero_or_negative():
    with pytest.raises(ValueError):
        validate_positive_int("0")
    with pytest.raises(ValueError):
        validate_positive_int("-3")


def test_validate_positive_int_rejects_non_numeric():
    with pytest.raises(ValueError):
        validate_positive_int("not-a-number")


def test_validate_port_rejects_out_of_range():
    with pytest.raises(ValueError):
        validate_port("70000")


def test_validate_host_rejects_empty():
    with pytest.raises(ValueError):
        validate_host("   ")


def test_validate_host_accepts_ip_and_hostname():
    assert validate_host("127.0.0.1") == "127.0.0.1"
    assert validate_host("example.com") == "example.com"


def test_human_bytes_formats_reasonably():
    assert human_bytes(500) == "500 B"
    assert "KB" in human_bytes(2048)


def test_hash_file_is_deterministic(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("hello world")
    assert hash_file(str(f)) == hash_file(str(f))


# ---------------------------------------------------------------------------
# models.py
# ---------------------------------------------------------------------------

def test_connection_from_row_valid():
    row = {"timestamp": "t", "src_ip": "1.2.3.4", "dst_port": "80", "protocol": "tcp", "bytes": "10"}
    conn = Connection.from_row(row)
    assert conn.dst_port == 80
    assert conn.num_bytes == 10


def test_connection_from_row_rejects_bad_port():
    row = {"timestamp": "t", "src_ip": "1.2.3.4", "dst_port": "not-a-port", "protocol": "tcp", "bytes": "10"}
    with pytest.raises(ValueError):
        Connection.from_row(row)


# ---------------------------------------------------------------------------
# logic.py -- log analysis
# ---------------------------------------------------------------------------

def test_count_protocols(sample_connections):
    counts = count_protocols(sample_connections)
    assert counts["tcp"] == 3
    assert counts["udp"] == 1


def test_find_watchlist_hits(sample_connections):
    hits = find_watchlist_hits(sample_connections, watchlist_ports=[4444, 8080])
    hit_ports = {h["dst_port"] for h in hits}
    assert hit_ports == {4444, 8080}


def test_find_watchlist_hits_empty_watchlist(sample_connections):
    assert find_watchlist_hits(sample_connections, watchlist_ports=[]) == []


def test_find_top_talker(sample_connections):
    top = find_top_talker(sample_connections)
    assert top["src_ip"] == "10.0.0.5"
    assert top["total_bytes"] == 9500


def test_find_top_talker_empty_list_returns_none():
    assert find_top_talker([]) is None


# ---------------------------------------------------------------------------
# logic.py -- filesystem scanning
# ---------------------------------------------------------------------------

def test_scan_folder_counts_files(evidence_folder):
    artifacts = scan_folder(evidence_folder)
    assert len(artifacts) == 4


def test_find_duplicates_groups_identical_content(evidence_folder):
    artifacts = scan_folder(evidence_folder)
    duplicates = find_duplicates(artifacts)
    assert len(duplicates) == 1
    assert set(duplicates[0]) == {"a.txt", "b.txt"}


def test_flag_recent_files_excludes_old_file(evidence_folder):
    artifacts = scan_folder(evidence_folder)
    recent = flag_recent_files(artifacts, window_seconds=60)
    recent_names = {r["name"] for r in recent}
    assert "old.txt" not in recent_names
    # a.txt/b.txt/c.txt were just created, so they should be "recent"
    assert {"a.txt", "b.txt", "c.txt"}.issubset(recent_names)


# ---------------------------------------------------------------------------
# logic.py -- port scanning
# ---------------------------------------------------------------------------

def test_check_port_closed_on_unused_local_port():
    # Port 1 is a privileged, essentially-never-open port -- safe to assume closed.
    result = check_port("127.0.0.1", 1, timeout=0.2)
    assert result.host == "127.0.0.1"
    assert result.is_open is False


def test_scan_port_range_validates_order():
    with pytest.raises(ValueError):
        scan_port_range("127.0.0.1", 100, 1)


def test_scan_port_range_rejects_bad_host():
    with pytest.raises(ValueError):
        scan_port_range("   ", 1, 5)


# ---------------------------------------------------------------------------
# logic.py -- report assembly
# ---------------------------------------------------------------------------

def test_build_report_with_no_data_adds_note():
    report = build_report(target="nothing")
    assert report.notes


def test_build_report_combines_sources(sample_connections, evidence_folder):
    artifacts = scan_folder(evidence_folder)
    report = build_report(
        target="combo",
        connections=sample_connections,
        watchlist_ports=[4444],
        artifacts=artifacts,
        recent_window_seconds=60,
    )
    assert report.protocol_counts
    assert len(report.watchlist_hits) == 1
    assert report.duplicate_groups
