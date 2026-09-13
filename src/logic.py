import psutil


def get_running_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "username", "exe", "status", "create_time"]
    ):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes


def analyze_process(process):
    reasons = []

    name = process.get("name") or ""
    exe = process.get("exe") or ""
    status = process.get("status") or ""

    if not name:
        reasons.append("Missing process name")

    if status != "running":
        reasons.append(f"Process status is {status}")

    suspicious_locations = [
        "\\AppData\\Local\\Temp\\",
        "\\Windows\\Temp\\",
    ]

    for location in suspicious_locations:
        if location.lower() in exe.lower():
            reasons.append("Executable is running from a temporary folder")
            break

    if reasons:
        risk = "REVIEW"
    else:
        risk = "NORMAL"

    return risk, reasons
from pathlib import Path
from datetime import datetime


def get_recent_files(directory, limit=20):
    files = []

    directory = Path(directory)

    for file_path in directory.rglob("*"):
        if file_path.is_file():
            try:
                modified_time = file_path.stat().st_mtime

                files.append({
                    "path": str(file_path),
                    "modified_time": modified_time
                })

            except (PermissionError, OSError):
                continue

    files.sort(key=lambda file: file["modified_time"], reverse=True)

    for file in files:
        file["modified_time"] = datetime.fromtimestamp(
            file["modified_time"]
        ).isoformat()

    return files[:limit]