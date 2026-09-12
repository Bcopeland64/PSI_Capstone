"""Core triage logic."""

import os
import subprocess

from .utils import hash_file, get_file_metadata


def check_processes(limit=10):
    """Return a small read-only sample of running processes.

    psutil is preferred because it works across platforms. If it is not
    installed, a platform-appropriate read-only command is used.
    """
    try:
        import psutil

        processes = []
        for process in psutil.process_iter(["pid", "name"]):
            try:
                processes.append(process.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes[:limit]

    except ImportError:
        try:
            if os.name == "nt":
                command = ["tasklist"]
            else:
                command = ["ps", "aux"]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.stdout.splitlines()[:limit]

        except (OSError, subprocess.SubprocessError) as error:
            return [f"Process listing unavailable: {error}"]


def check_hashes(folder):
    """Return a list containing file metadata and SHA-256 hashes."""
    results = []

    for name in os.listdir(folder):
        path = os.path.join(folder, name)

        if not os.path.isfile(path):
            continue

        try:
            metadata = get_file_metadata(path)
            metadata["sha256"] = hash_file(path)
            results.append(metadata)
        except (OSError, PermissionError) as error:
            print(f"Warning: could not hash '{path}': {error}")

    return results


def build_timeline(folder):
    """Build and sort a simple file timeline."""
    timeline = check_hashes(folder)
    timeline.sort(key=lambda item: item["modified"])
    return timeline


def run_triage(folder, window_seconds=600):
    """Collect processes, recent files, hashes, and a file timeline."""
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"'{folder}' is not a valid folder.")

    return {
        "folder": os.path.abspath(folder),
        "processes": check_processes(),
        "recent_files": __import__(
            "src.utils", fromlist=["check_recent_files"]
        ).check_recent_files(folder, window_seconds),
        "file_hashes": check_hashes(folder),
        "timeline": build_timeline(folder),
    }
