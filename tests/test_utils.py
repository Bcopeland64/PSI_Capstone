import pytest

from src.utils import validate_directory


def test_valid_directory(tmp_path):
    """Test that a non-empty directory passes validation."""

    test_file = tmp_path / "evidence.txt"
    test_file.write_text("evidence", encoding="utf-8")

    validate_directory(str(tmp_path))


def test_missing_directory(tmp_path):
    """Test that a missing directory raises FileNotFoundError."""

    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        validate_directory(str(missing_directory))


def test_empty_directory(tmp_path):
    """Test that an empty directory raises ValueError."""

    with pytest.raises(ValueError):
        validate_directory(str(tmp_path))