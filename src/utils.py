"""Utility functions for the triage application."""

import hashlib
import os
import time
from pathlib import Path


def hash_file(path):
    """Return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_metadata(path):
    """Return basic metadata for a file."""
    stat_result = os.stat(path)
    return {
        "name": Path(path).name,
        "path": str(path),
        "size": stat_result.st_size,
        "modified": stat_result.st_mtime,
    }


def check_recent_files(folder, window_seconds=600):
    """Return file metadata for files modified within the time window."""
    current_time = time.time()
    recent = []

    for name in os.listdir(folder):
        path = os.path.join(folder, name)

        if not os.path.isfile(path):
            continue

        try:
            metadata = get_file_metadata(path)
            age = current_time - metadata["modified"]

            if 0 <= age <= window_seconds:
                metadata["age_seconds"] = int(age)
                recent.append(metadata)
        except OSError as error:
            print(f"Warning: could not inspect '{path}': {error}")

    recent.sort(key=lambda item: item["modified"])
    return recent
