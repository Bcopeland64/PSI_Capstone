"""Validation and helper functions."""

import ipaddress
import os


def validate_file_path(file_path: str) -> str:
    """Validate that a supplied path exists and is readable."""
    if not file_path or not file_path.strip():
        raise ValueError("Log file path cannot be empty.")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Log file was not found: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Log file is not readable: {file_path}")

    return file_path


def validate_threshold(value: int) -> int:
    """Validate that the suspicious-IP threshold is a positive integer."""
    try:
        threshold = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Threshold must be an integer.") from exc

    if threshold < 1:
        raise ValueError("Threshold must be at least 1.")

    return threshold


def is_valid_ip(value: str) -> bool:
    """Return True if the supplied value is a valid IP address."""
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
