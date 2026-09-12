import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from logic import clean_data, analyze


def test_clean_data_removes_bad_rows():
    """Rows with non-numeric bytes should be dropped."""
    df = pd.DataFrame({
        "src_ip": ["10.0.0.1", "10.0.0.2"],
        "bytes": ["100", "not_a_number"],
        "status": ["ok", "ok"],
    })
    cleaned = clean_data(df)
    assert len(cleaned) == 1


def test_analyze_finds_top_talker():
    """The IP sending the most bytes should be flagged as top talker."""
    df = pd.DataFrame({
        "src_ip": ["10.0.0.1", "10.0.0.1", "10.0.0.2"],
        "bytes": [500, 500, 100],
        "status": ["ok", "ok", "ok"],
    })
    results = analyze(df)
    assert results["top_talker"] == "10.0.0.1"
    assert results["top_bytes"] == 1000

def test_analyze_flags_repeated_failures():
    """An IP with repeated failures and a high failure rate should be flagged."""
    df = pd.DataFrame({
        "src_ip": [
            "10.0.0.7",
            "10.0.0.7",
            "10.0.0.7",
            "10.0.0.8"
        ],
        "dst_port": [8080, 8080, 8080, 22],
        "bytes": [100, 100, 100, 50],
        "status": ["failed", "failed", "failed", "failed"],
    })

    results = analyze(df)

    assert len(results["suspicious_ips"]) == 1
    assert results["suspicious_ips"][0]["ip"] == "10.0.0.7"
    assert results["suspicious_ips"][0]["failed_attempts"] == 3
    assert results["suspicious_ips"][0]["failure_rate"] == 1.0