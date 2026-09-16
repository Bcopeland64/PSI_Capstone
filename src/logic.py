"""
logic.py
--------
Core business logic for the capstone project:

- WebScraper   : ethically fetches a web page and extracts structured
                 data (links + word-frequency stats).
- LogAnalyzer  : re-uses the Day 1 log-parsing / regex techniques to
                 analyze a text log file (e.g. failed-login counting,
                 IP extraction, per-level tallies).
- DataStore    : handles data persistence to CSV and JSON.

Together these combine OOP design, external package integration
(requests, BeautifulSoup), data persistence, and error handling,
as required by the capstone brief.
"""

import csv
import json
import os
import re
from collections import Counter

from bs4 import BeautifulSoup

from src import utils


class WebScraper:
    """
    A small, ethical web scraper.

    "Ethical" here means: it identifies itself with a User-Agent,
    only ever performs GET requests, respects HTTP errors instead of
    hammering a failing endpoint, and does not bypass any access
    controls -- it simply parses whatever public HTML is returned.
    """

    def __init__(self, url: str):
        self.url = utils.validate_url(url)
        self.html = None

    def fetch(self) -> bool:
        """Fetch the page HTML. Returns True on success, False otherwise."""
        response = utils.safe_request(self.url)
        if response is None:
            return False
        self.html = response.text
        return True

    def extract_links(self) -> list:
        """Return a sorted list of unique absolute-or-relative links (<a href>)."""
        if not self.html:
            raise RuntimeError("No HTML loaded. Call fetch() first.")

        soup = BeautifulSoup(self.html, "html.parser")
        links = {a["href"] for a in soup.find_all("a", href=True)}
        return sorted(links)

    def word_frequency(self, top_n: int = 10) -> list:
        """
        Return the `top_n` most common words found in the page's visible
        text, as (word, count) tuples -- reusing the Counter pattern
        from Day 1/Day 2 of the workshop.
        """
        if not self.html:
            raise RuntimeError("No HTML loaded. Call fetch() first.")

        soup = BeautifulSoup(self.html, "html.parser")
        text = soup.get_text(separator=" ").lower()
        words = re.findall(r"[a-zA-Z]{3,}", text)
        return Counter(words).most_common(top_n)

    def scrape(self) -> dict:
        """
        Orchestrate fetch + parse and return a single summary record,
        ready to be persisted by DataStore.
        """
        if not self.fetch():
            raise ConnectionError(f"Could not fetch '{self.url}'.")

        links = self.extract_links()
        top_words = self.word_frequency(top_n=5)

        return {
            "url": self.url,
            "link_count": len(links),
            "top_words": "; ".join(f"{w}({c})" for w, c in top_words),
            "html_size_bytes": len(self.html.encode("utf-8")),
        }


class LogAnalyzer:
    """
    Analyzes a plain-text log file using the file-reading, regex and
    Counter techniques from Day 1 (log parsing) and Day 2/3
    (structured artifact analysis).
    """

    IP_PATTERN = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def __init__(self, log_path: str):
        if not os.path.isfile(log_path):
            raise FileNotFoundError(f"Log file not found: '{log_path}'")
        self.log_path = log_path

    def count_keyword(self, keyword: str) -> int:
        """Count how many lines contain `keyword` (case-sensitive, as in Day 1)."""
        with open(self.log_path, encoding="utf-8", errors="ignore") as f:
            return sum(1 for line in f if keyword in line)

    def extract_ips(self) -> list:
        """Return every IP address found anywhere in the log file."""
        with open(self.log_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return self.IP_PATTERN.findall(text)

    def top_ips(self, n: int = 5) -> list:
        """Return the `n` most frequently occurring IP addresses."""
        return Counter(self.extract_ips()).most_common(n)

    def level_tally(self) -> dict:
        """
        Tally lines by common log level keywords (INFO/WARNING/ERROR),
        falling back to 0 for levels that never appear.
        """
        levels = ("INFO", "WARNING", "ERROR")
        return {level: self.count_keyword(level) for level in levels}

    def generate_report(self) -> dict:
        """Combine the analyses above into a single summary dict."""
        return {
            "log_file": self.log_path,
            "failed_password_lines": self.count_keyword("Failed password"),
            "level_tally": self.level_tally(),
            "top_ips": self.top_ips(),
        }


class DataStore:
    """Handles reading and writing project data to CSV / JSON files."""

    @staticmethod
    def save_to_csv(records: list, path: str) -> None:
        """
        Write a list of flat dicts to a CSV file. Raises ValueError if
        `records` is empty, since there would be no header to write.
        """
        if not records:
            raise ValueError("Cannot write an empty list of records to CSV.")

        utils.ensure_directory(os.path.dirname(path) or ".")
        fieldnames = list(records[0].keys())

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    @staticmethod
    def load_from_csv(path: str) -> list:
        """Load a CSV file back into a list of dicts."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No such CSV file: '{path}'")

        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def save_to_json(data, path: str) -> None:
        """Write `data` (any JSON-serializable object) to a JSON file."""
        utils.ensure_directory(os.path.dirname(path) or ".")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_from_json(path: str):
        """Load and return the JSON content at `path`."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No such JSON file: '{path}'")
        with open(path, encoding="utf-8") as f:
            return json.load(f)
