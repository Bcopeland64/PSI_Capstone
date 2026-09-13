import hashlib

from src.scanner import calculate_sha256, scan_directory


def test_calculate_sha256(tmp_path):
    """Test SHA-256 calculation for a known file."""

    test_file = tmp_path / "evidence.txt"
    test_file.write_text("hello", encoding="utf-8")

    expected_hash = hashlib.sha256(b"hello").hexdigest()

    result = calculate_sha256(str(test_file))

    assert result == expected_hash


def test_scan_directory(tmp_path):
    """Test that files in a directory are discovered."""

    test_file = tmp_path / "sample.log"
    test_file.write_text("sample evidence", encoding="utf-8")

    results = scan_directory(str(tmp_path))

    assert len(results) == 1
    assert results[0].name == "sample.log"
    assert results[0].extension == ".log"