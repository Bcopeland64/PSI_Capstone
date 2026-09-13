"""Basic unit tests for the capstone triage tool."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from src.logic import build_timeline
from src.utils import check_recent_files, hash_file


class TestTriageLogic(unittest.TestCase):
    def test_hash_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.txt"
            content = "hello triage"
            path.write_text(content, encoding="utf-8")

            expected = hashlib.sha256(content.encode()).hexdigest()
            self.assertEqual(hash_file(path), expected)

    def test_build_timeline_contains_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            (folder / "one.txt").write_text("one", encoding="utf-8")
            (folder / "two.txt").write_text("two", encoding="utf-8")

            timeline = build_timeline(folder)
            names = {item["name"] for item in timeline}

            self.assertEqual(names, {"one.txt", "two.txt"})

    def test_recent_files_with_large_window(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            (folder / "recent.txt").write_text("recent", encoding="utf-8")

            recent = check_recent_files(folder, window_seconds=600)
            names = {item["name"] for item in recent}

            self.assertIn("recent.txt", names)


if __name__ == "__main__":
    unittest.main()
