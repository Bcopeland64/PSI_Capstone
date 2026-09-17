import hashlib
import os
import time
from collections import defaultdict

from .models import FileEvidence, ProcessInfo


def hash_file(path):
    """Return the SHA-256 hash of a file."""
    try:
        with open(path, "rb") as file:
            return hashlib.sha256(file.read()).hexdigest()
    except OSError as error:
        print(f"Could not hash {path}: {error}")
        return None


def get_file_evidence(folder, window_seconds=600):
    """Collect metadata and hashes for files in a folder."""
    evidence = []
    current_time = time.time()

    try:
        names = os.listdir(folder)
    except OSError as error:
        print(f"Could not read folder: {error}")
        return evidence

    for name in names:
        path = os.path.join(folder, name)

        if not os.path.isfile(path):
            continue

        try:
            stat_result = os.stat(path)
            file_hash = hash_file(path)

            if file_hash is None:
                continue

            age = current_time - stat_result.st_mtime
            recent = age <= window_seconds

            evidence.append(
                FileEvidence(
                    name=name,
                    size=stat_result.st_size,
                    modified_time=stat_result.st_mtime,
                    sha256=file_hash,
                    recent=recent,
                )
            )

        except OSError as error:
            print(f"Could not inspect {name}: {error}")

    evidence.sort(key=lambda item: item.modified_time)

    return evidence


def check_processes(limit=10):
    """Return a list of currently running processes."""
    processes = []

    try:
        import psutil

        for process in psutil.process_iter(["pid", "name"]):
            try:
                info = process.info
                processes.append(
                    ProcessInfo(
                        pid=info["pid"],
                        name=info["name"] or "Unknown",
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

            if len(processes) >= limit:
                break

    except ImportError:
        print("psutil is not installed. Process check skipped.")

    return processes


def find_duplicates(folder):
    """Find files that have identical SHA-256 hashes."""
    hash_groups = defaultdict(list)

    try:
        names = os.listdir(folder)
    except OSError as error:
        print(f"Could not read folder: {error}")
        return {}

    for name in names:
        path = os.path.join(folder, name)

        if not os.path.isfile(path):
            continue

        file_hash = hash_file(path)

        if file_hash:
            hash_groups[file_hash].append(name)

    duplicates = {
        file_hash: names
        for file_hash, names in hash_groups.items()
        if len(names) > 1
    }

    return duplicates


def check_port(host="127.0.0.1", port=80):
    """Check if a TCP port is open."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False
    finally:
        s.close()
        

def run_command(cmd):
    """Run a system command and return output."""
    import subprocess
    if not isinstance(cmd, (list, str)):
        return f"Invalid command type: {type(cmd)}. Must be str or list."
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running {cmd}: {e}"
        

def check_url(url):
    """Check HTTP status of a URL."""
    import requests
    try:
        r = requests.get(url, timeout=3)
        return r.status_code
    except requests.RequestException as e:
        return f"Error: {e}"
