"""
utils.py
--------
Helper functions for validating raw CSV rows before they become alerts.
"""

import re

REQUIRED_COLUMNS = {"timestamp", "source_ip", "username", "event_type", "failed_attempts"}

# Simple pattern to check something looks like an IPv4 address
_IP_PATTERN = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")


def is_valid_ip(ip_address: str) -> bool:
    """Return True if ip_address looks like a valid IPv4 address."""
    match = _IP_PATTERN.match(ip_address.strip())
    if not match:
        return False
    # Each part must be a number between 0 and 255
    return all(0 <= int(part) <= 255 for part in match.groups())


def validate_row(row: dict) -> tuple[bool, str]:
    """
    Check whether a raw CSV row (a dict) has everything it needs to become
    a valid alert.
    """
    # Check all required columns are present
    missing = REQUIRED_COLUMNS - row.keys()
    if missing:
        return False, f"Missing column(s): {', '.join(missing)}"

    # Check the IP address looks valid
    if not is_valid_ip(row["source_ip"]):
        return False, f"Invalid IP address: {row['source_ip']}"

    # Check failed_attempts can actually become a number
    try:
        attempts = int(row["failed_attempts"])
        if attempts < 0:
            return False, "failed_attempts cannot be negative"
    except ValueError:
        return False, f"failed_attempts is not a number: {row['failed_attempts']}"

    # Check username and event_type aren't blank
    if not row["username"].strip():
        return False, "username is empty"
    if not row["event_type"].strip():
        return False, "event_type is empty"

    return True, ""