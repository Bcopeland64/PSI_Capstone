from pathlib import Path

from src.logic import find_duplicates, hash_file


def test_hash_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    result = hash_file(str(test_file))

    assert result is not None
    assert len(result) == 64


def test_find_duplicates(tmp_path):
    file1 = Path(tmp_path) / "one.txt"
    file2 = Path(tmp_path) / "two.txt"

    file1.write_text("same content")
    file2.write_text("same content")

    duplicates = find_duplicates(str(tmp_path))

    assert len(duplicates) == 1
    assert set(next(iter(duplicates.values()))) == {
        "one.txt",
        "two.txt",
    }