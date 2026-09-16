"""
test_logic.py
-------------
Unit tests for the pieces of logic.py that don't require network
access: LogAnalyzer, DataStore, and WebScraper's pure-parsing methods
(fed with local HTML instead of a live request).
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logic import DataStore, LogAnalyzer, WebScraper

SAMPLE_LOG = os.path.join(os.path.dirname(__file__), "..", "data", "sample_auth.log")


# ---------- LogAnalyzer ----------

def test_log_analyzer_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        LogAnalyzer("no_such_file.log")


def test_count_keyword_failed_password():
    analyzer = LogAnalyzer(SAMPLE_LOG)
    assert analyzer.count_keyword("Failed password") == 5


def test_extract_ips_finds_all_ips():
    analyzer = LogAnalyzer(SAMPLE_LOG)
    ips = analyzer.extract_ips()
    assert "45.33.12.9" in ips
    assert "91.198.174.2" in ips
    assert len(ips) == 7  # one IP per log line


def test_top_ips_orders_by_frequency():
    analyzer = LogAnalyzer(SAMPLE_LOG)
    top = analyzer.top_ips(1)
    assert top[0][0] == "45.33.12.9"
    assert top[0][1] == 3


def test_generate_report_shape():
    analyzer = LogAnalyzer(SAMPLE_LOG)
    report = analyzer.generate_report()
    assert report["failed_password_lines"] == 5
    assert "level_tally" in report
    assert isinstance(report["top_ips"], list)


# ---------- DataStore ----------

def test_save_and_load_csv_roundtrip(tmp_path):
    records = [
        {"url": "https://a.test", "link_count": "2"},
        {"url": "https://b.test", "link_count": "5"},
    ]
    csv_path = str(tmp_path / "out.csv")

    DataStore.save_to_csv(records, csv_path)
    loaded = DataStore.load_from_csv(csv_path)

    assert loaded == records


def test_save_to_csv_empty_records_raises():
    with pytest.raises(ValueError):
        DataStore.save_to_csv([], "/tmp/should_not_be_created.csv")


def test_save_and_load_json_roundtrip(tmp_path):
    data = {"hello": "world", "count": 3}
    json_path = str(tmp_path / "out.json")

    DataStore.save_to_json(data, json_path)
    loaded = DataStore.load_from_json(json_path)

    assert loaded == data


def test_load_from_json_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        DataStore.load_from_json("no_such_file.json")


# ---------- WebScraper (pure parsing, no network) ----------

SAMPLE_HTML = """
<html><body>
<a href="/about">About</a>
<a href="https://example.com/contact">Contact</a>
<a href="/about">About</a>
<p>Python security python SECURITY testing testing testing</p>
</body></html>
"""


def test_word_frequency_counts_case_insensitively():
    scraper = WebScraper("https://example.com")
    scraper.html = SAMPLE_HTML
    freq = dict(scraper.word_frequency(top_n=10))
    assert freq["testing"] == 3
    assert freq["python"] == 2
    assert freq["security"] == 2


def test_extract_links_deduplicates():
    scraper = WebScraper("https://example.com")
    scraper.html = SAMPLE_HTML
    links = scraper.extract_links()
    assert links == ["/about", "https://example.com/contact"]


def test_scraper_rejects_invalid_url():
    with pytest.raises(ValueError):
        WebScraper("not-a-url")
