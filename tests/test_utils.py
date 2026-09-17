"""Tests for sectriage.utils.

Written with the standard-library `unittest` module so they run with zero
extra dependencies (`python -m unittest discover`), and are also picked up
automatically by `pytest` if it's installed, since pytest discovers
unittest.TestCase classes too.
"""

import os
import tempfile
import unittest

from sectriage.exceptions import InvalidTargetError
from sectriage.utils import ensure_parent_dir, hash_file, human_age, iter_files


class TestHashFile(unittest.TestCase):
    def test_known_content_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sample.txt")
            with open(path, "w") as handle:
                handle.write("hello world")
            self.assertNotEqual(hash_file(path), "")  # sanity: something was computed
            self.assertEqual(len(hash_file(path)), 64)  # sha256 hex digest length

    def test_same_content_same_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path_a = os.path.join(tmp, "a.txt")
            path_b = os.path.join(tmp, "b.txt")
            for path in (path_a, path_b):
                with open(path, "w") as handle:
                    handle.write("duplicate content")
            self.assertEqual(hash_file(path_a), hash_file(path_b))

    def test_missing_file_raises(self):
        with self.assertRaises(InvalidTargetError):
            hash_file("/no/such/file/anywhere.txt")


class TestIterFiles(unittest.TestCase):
    def test_missing_folder_raises(self):
        with self.assertRaises(InvalidTargetError):
            list(iter_files("/no/such/folder"))

    def test_lists_files_not_subfolders(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.txt"), "w").close()
            os.makedirs(os.path.join(tmp, "subdir"))
            files = list(iter_files(tmp))
            self.assertEqual(len(files), 1)
            self.assertTrue(files[0].endswith("a.txt"))


class TestHumanAge(unittest.TestCase):
    def test_seconds(self):
        self.assertEqual(human_age(45), "45s ago")

    def test_minutes(self):
        self.assertEqual(human_age(125), "2m 5s ago")

    def test_hours(self):
        self.assertEqual(human_age(3725), "1h 2m ago")


class TestEnsureParentDir(unittest.TestCase):
    def test_creates_missing_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "deeper", "out.json")
            ensure_parent_dir(target)
            self.assertTrue(os.path.isdir(os.path.dirname(target)))


if __name__ == "__main__":
    unittest.main()
