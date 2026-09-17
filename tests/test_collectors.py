"""Tests for sectriage.collectors."""

import os
import tempfile
import time
import unittest

from sectriage.collectors import FileSystemCollector, LogAnalyzer, NetworkAnalyzer
from sectriage.exceptions import InvalidTargetError, UnsupportedFormatError


class TestFileSystemCollector(unittest.TestCase):
    def setUp(self):
        self.collector = FileSystemCollector()

    def test_scan_returns_one_record_per_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "one.txt"), "w").close()
            open(os.path.join(tmp, "two.txt"), "w").close()
            records = self.collector.scan(tmp)
            self.assertEqual(len(records), 2)
            self.assertEqual({r.name for r in records}, {"one.txt", "two.txt"})

    def test_find_duplicates_groups_identical_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("original.bin", "renamed_copy.bin"):
                with open(os.path.join(tmp, name), "w") as handle:
                    handle.write("identical payload")
            with open(os.path.join(tmp, "unique.bin"), "w") as handle:
                handle.write("something else entirely")

            duplicates = self.collector.find_duplicates(tmp)
            self.assertEqual(len(duplicates), 1)
            group = list(duplicates.values())[0]
            self.assertEqual(set(group), {"original.bin", "renamed_copy.bin"})

    def test_recent_respects_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "fresh.txt"), "w").close()
            recent = self.collector.recent(tmp, window_seconds=3600)
            self.assertEqual(len(recent), 1)
            stale = self.collector.recent(tmp, window_seconds=0)
            # A file created "now" should not be older than a 0-second window.
            self.assertEqual(len(stale), 0)

    def test_missing_folder_raises(self):
        with self.assertRaises(InvalidTargetError):
            self.collector.scan("/definitely/not/a/real/folder")


class TestLogAnalyzer(unittest.TestCase):
    def test_counts_levels_and_failed_logins(self):
        content = (
            "Jan  4 09:10:22 srv sshd: Failed password for root from 45.33.12.9\n"
            "Jan  4 09:10:24 srv sshd: Failed password for root from 45.33.12.9\n"
            "Jan  4 09:12:40 srv kernel: WARNING Disk usage at 82% on host 10.0.0.5\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "auth.log")
            with open(path, "w") as handle:
                handle.write(content)

            summary = LogAnalyzer().analyze(path)
            self.assertEqual(summary.total_lines, 3)
            self.assertEqual(summary.level_counts.get("WARNING"), 1)
            self.assertIn("45.33.12.9", summary.unique_ips)
            self.assertEqual(summary.top_offenders[0], ("45.33.12.9", 2))

    def test_missing_file_raises(self):
        with self.assertRaises(InvalidTargetError):
            LogAnalyzer().analyze("/no/such/log.log")

    def test_write_filtered(self):
        content = "keep this ERROR line\nskip this INFO line\nkeep another ERROR line\n"
        with tempfile.TemporaryDirectory() as tmp:
            in_path = os.path.join(tmp, "in.log")
            out_path = os.path.join(tmp, "out.log")
            with open(in_path, "w") as handle:
                handle.write(content)

            count = LogAnalyzer().write_filtered(in_path, out_path, "ERROR")
            self.assertEqual(count, 2)
            with open(out_path) as handle:
                self.assertEqual(len(handle.readlines()), 2)


class TestNetworkAnalyzer(unittest.TestCase):
    def test_analyze_csv_flags_suspicious_ports(self):
        content = (
            "timestamp,src_ip,dst_port,protocol,bytes\n"
            "2026-01-04T09:00:01,10.0.0.5,443,tcp,1200\n"
            "2026-01-04T09:00:20,10.0.0.9,4444,tcp,900\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "traffic.csv")
            with open(path, "w") as handle:
                handle.write(content)

            summary = NetworkAnalyzer().analyze_csv(path)
            self.assertEqual(summary.total_rows, 2)
            self.assertEqual(len(summary.suspicious_hits), 1)
            self.assertEqual(summary.suspicious_hits[0]["dst_port"], "4444")

    def test_missing_columns_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.csv")
            with open(path, "w") as handle:
                handle.write("a,b,c\n1,2,3\n")
            with self.assertRaises(UnsupportedFormatError):
                NetworkAnalyzer().analyze_csv(path)

    def test_missing_file_raises(self):
        with self.assertRaises(InvalidTargetError):
            NetworkAnalyzer().analyze_csv("/no/such/traffic.csv")


if __name__ == "__main__":
    unittest.main()
