"""
logic.py
--------
Reads alerts from a CSV file, classifies them, and groups them by source IP.
"""

import csv
import json
import os

from src.models import make_alert, classify_alert, make_source_summary
from src.utils import validate_row


def load_alerts(csv_path: str) -> list:
    """
    Read a CSV file and return a list of alert dicts.
    Invalid rows are skipped and a warning is printed, instead of
    crashing the whole program.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    alerts = []
    skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reads each row as a dict automatically
        for row in reader:
            is_valid, error = validate_row(row)
            if not is_valid:
                print(f"Skipping bad row: {error}")
                skipped += 1
                continue

            alert = make_alert(
                timestamp=row["timestamp"],
                source_ip=row["source_ip"].strip(),
                username=row["username"].strip(),
                event_type=row["event_type"].strip(),
                failed_attempts=int(row["failed_attempts"]),
            )
            alerts.append(alert)

    print(f"Loaded {len(alerts)} valid alert(s), skipped {skipped}.")
    return alerts


def classify_all(alerts: list) -> None:
    """Classify every alert in the list (modifies them in place)."""
    for alert in alerts:
        classify_alert(alert)


def summarize_by_source(alerts: list) -> list:
    """
    Group alerts by source_ip and build one summary dict per IP:
    total failed attempts, distinct event types, and the worst
    severity seen for that IP.
    """
    grouped = {}  # {source_ip: [alert, alert, ...]}
    for alert in alerts:
        ip = alert["source_ip"]
        if ip not in grouped:
            grouped[ip] = []
        grouped[ip].append(alert)

    severity_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

    summaries = []
    for ip, group in grouped.items():
        total_attempts = sum(a["failed_attempts"] for a in group)
        event_types = [a["event_type"] for a in group]
        highest = max(group, key=lambda a: severity_rank[a["severity"]])["severity"]

        summary = make_source_summary(
            source_ip=ip,
            total_failed_attempts=total_attempts,
            event_types=event_types,
            highest_severity=highest,
            alert_count=len(group),
        )
        summaries.append(summary)

    return summaries


def export_report(summaries: list, output_path: str) -> None:
    """Save a list of summary dicts to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)
    print(f"Report saved to {output_path}")