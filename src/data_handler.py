import csv
import json
from collections import Counter


def read_artifacts(csv_path):
    """Read forensic artifacts from a CSV file."""
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"Artifact file not found: {csv_path}")
        return []
    except OSError as error:
        print(f"Could not read artifact file: {error}")
        return []


def analyze_artifacts(rows):
    """Return useful statistics from artifact rows."""
    if not rows:
        return {
            "total_events": 0,
            "by_type": {},
            "by_hour": {},
        }

    by_type = Counter(row.get("event_type", "unknown") for row in rows)

    by_hour = Counter()

    for row in rows:
        timestamp = row.get("timestamp", "")

        if len(timestamp) >= 13:
            hour = timestamp[11:13]
            by_hour[hour] += 1

    return {
        "total_events": len(rows),
        "by_type": dict(by_type),
        "by_hour": dict(by_hour),
    }


def write_report(report, output_path):
    """Write the final triage report to a JSON file."""
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4, default=str)

        return True

    except OSError as error:
        print(f"Could not write report: {error}")
        return False