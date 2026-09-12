"""Reusable helper functions: hashing, port checks, and input validation.

These are the same primitives from the workshop's networking/OS-interaction
sections (hashlib + socket), wrapped with error handling so the rest of the
app can call them without worrying about missing files or bad input.
"""

from __future__ import annotations

import hashlib
import socket


def hash_file(path: str, algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    """Return the hex digest of a file, reading it in chunks.

    Reading in chunks (rather than one big .read()) keeps memory use flat
    even for large files. Raises FileNotFoundError / PermissionError as-is
    so callers can decide how to handle them.
    """
    hasher = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def port_status(host: str, port: int, timeout: float = 0.5) -> str:
    """Return 'open' or 'closed' for a single host:port using a TCP connect.

    Authorized-use note: only run this against hosts you own or are
    explicitly permitted to test (localhost / lab targets).
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host '{host}': {exc}") from exc
    finally:
        sock.close()
    return "open" if result == 0 else "closed"


def validate_port(raw_value: str) -> int:
    """Parse and validate a port number from user input.

    Raises ValueError with a friendly message if the input isn't a valid
    TCP/UDP port (1-65535).
    """
    try:
        port = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"'{raw_value}' is not a number.") from exc
    if not (1 <= port <= 65535):
        raise ValueError(f"Port {port} is out of range (must be 1-65535).")
    return port


def validate_non_empty(raw_value: str, field_name: str = "value") -> str:
    """Validate that user input isn't blank, returning the stripped value."""
    stripped = raw_value.strip()
    if not stripped:
        raise ValueError(f"{field_name} cannot be empty.")
    return stripped


def prompt_int(prompt_text: str, minimum: int | None = None, maximum: int | None = None) -> int:
    """Prompt the user until they enter a valid integer within bounds."""
    while True:
        raw = input(prompt_text).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"  Please enter a whole number (got '{raw}').")
            continue
        if minimum is not None and value < minimum:
            print(f"  Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"  Value must be at most {maximum}.")
            continue
        return value
