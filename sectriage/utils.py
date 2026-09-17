"""Small, reusable helper functions shared across collectors.

Keeping these here (instead of copy-pasting into every collector) is the
"Modular Code Architecture" and "Clean & Readable Code" requirement in
practice: one hashing implementation, one time-formatting implementation,
used everywhere.
"""

from __future__ import annotations

import hashlib
import os
import time
from typing import Iterator

from .exceptions import InvalidTargetError

# Chunk size for streaming file reads -- keeps memory flat even on large files.
_HASH_CHUNK_SIZE = 8192


def hash_file(path: str, algorithm: str = "sha256") -> str:
    """Return the hex digest of ``path`` using ``algorithm``.

    Reads the file in fixed-size chunks so multi-gigabyte evidence files
    don't get loaded into memory all at once.

    Raises:
        InvalidTargetError: if the file cannot be opened or read.
    """
    try:
        hasher = hashlib.new(algorithm)
    except ValueError as exc:  # unknown algorithm name
        raise InvalidTargetError(f"Unsupported hash algorithm: {algorithm!r}") from exc

    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(_HASH_CHUNK_SIZE), b""):
                hasher.update(chunk)
    except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
        raise InvalidTargetError(f"Could not hash '{path}': {exc}") from exc

    return hasher.hexdigest()


def iter_files(folder: str) -> Iterator[str]:
    """Yield full paths of every regular file directly inside ``folder``.

    Raises:
        InvalidTargetError: if ``folder`` does not exist or isn't a directory.
    """
    if not os.path.isdir(folder):
        raise InvalidTargetError(f"'{folder}' is not a folder.")

    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            yield path


def human_age(seconds: float) -> str:
    """Format a duration in seconds as a short, human-readable age string."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s ago"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s ago"
    if seconds < 86400:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m ago"
    return f"{seconds // 86400}d ago"


def now_iso() -> str:
    """Current local time as an ISO-8601 string, used for report timestamps."""
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def ensure_parent_dir(path: str) -> None:
    """Create the parent directory of ``path`` if it doesn't already exist."""
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
