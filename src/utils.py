"""
utils.py
--------
Small, reusable helpers: input validation, hashing, and formatting.
Nothing in here reads a full report or writes a file — that belongs in
data_handler.py / logic.py. Keeping this module dependency-light means it can
be unit tested in isolation.
"""

import hashlib
import ipaddress
import os
from typing import Iterable


def validate_positive_int(value: str, field_name: str = "value") -> int:
    """Parse `value` as a positive integer, raising a friendly error otherwise.

    Args:
        value: the raw string (e.g. from argparse or user input).
        field_name: used in the error message so callers get useful feedback.

    Returns:
        The parsed integer.

    Raises:
        ValueError: if value is not a positive integer.
    """
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an integer, got {value!r}") from exc
    if parsed <= 0:
        raise ValueError(f"{field_name} must be a positive integer, got {parsed}")
    return parsed


def validate_port(value) -> int:
    """Validate that `value` is a usable TCP/UDP port number (1-65535)."""
    port = validate_positive_int(value, field_name="port")
    if port > 65535:
        raise ValueError(f"port must be between 1 and 65535, got {port}")
    return port


def validate_host(value: str) -> str:
    """Validate a host string is either a valid IP address or a non-empty hostname.

    We don't resolve the hostname here (that would require a network call and
    could be slow/flaky in a validator) -- we just guard against empty input.
    """
    if not value or not value.strip():
        raise ValueError("host must not be empty")
    value = value.strip()
    try:
        ipaddress.ip_address(value)
    except ValueError:
        # Not a literal IP -- accept it as a hostname if it looks sane.
        if any(ch.isspace() for ch in value):
            raise ValueError(f"host {value!r} looks invalid (contains whitespace)")
    return value


def validate_existing_path(path: str) -> str:
    """Confirm a filesystem path exists, raising FileNotFoundError with context otherwise."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"path does not exist: {path}")
    return path


def hash_file(path: str, chunk_size: int = 65536) -> str:
    """Return the SHA-256 hex digest of the file at `path`, reading in chunks.

    Reading in chunks (instead of file.read() all at once) keeps memory usage
    flat even for large evidence files.
    """
    sha256 = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def human_bytes(num_bytes: int) -> str:
    """Format a byte count as a short human-readable string (e.g. '1.4 KB')."""
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def chunked(iterable: Iterable, size: int):
    """Yield successive `size`-length chunks from `iterable` (used for batch output)."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
