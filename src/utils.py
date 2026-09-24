"""Validation, cleaning, and general utility functions."""

import ipaddress
from datetime import datetime


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

REQUIRED_FIELDS = (
    "incident_id",
    "timestamp",
    "source_ip",
    "destination_ip",
    "attack_type",
    "username",
    "description",
)


def clean_text(value: object) -> str:
    """Convert a value to trimmed text."""
    return str(value).strip()


def validate_ip(ip: str) -> bool:
    """Return True when the value is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def parse_timestamp(value: str) -> datetime:
    """Parse a timestamp using the application's expected format."""
    try:
        return datetime.strptime(value, TIMESTAMP_FORMAT)
    except ValueError as exc:
        raise ValueError(
            f"Invalid timestamp '{value}'. Expected format "
            f"YYYY-MM-DD HH:MM:SS."
        ) from exc


def validate_required_fields(row: dict) -> None:
    """Raise ValueError when a required field is missing or empty."""
    for field in REQUIRED_FIELDS:
        value = row.get(field)
        if value is None or not clean_text(value):
            raise ValueError(f"Missing required field: {field}")


def validate_incident_id(incident_id: str) -> None:
    """Validate the incident identifier."""
    if not incident_id:
        raise ValueError("Incident ID cannot be empty.")
    if len(incident_id) > 50:
        raise ValueError("Incident ID must not exceed 50 characters.")
