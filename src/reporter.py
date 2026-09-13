import csv
import json
import os
from datetime import datetime, timezone

from src.models import TriageResult


def save_csv_report(
    triage_results: list[TriageResult],
    output_path: str,
) -> None:
    """Save a clear, analyst-friendly triage report to CSV."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "File Name",
            "File Type",
            "Risk Level",
            "Risk Score",
            "Failed Logins",
            "Warnings",
            "Errors",
            "Critical Events",
            "Denied Events",
            "Unique IP Addresses",
            "Size (Bytes)",
            "Last Modified (UTC)",
            "SHA-256",
            "File Path",
            "Reasons",
        ])

        for result in triage_results:
            evidence = result.evidence_file
            events = result.event_counts

            # Remove duplicate IP addresses while keeping their original order.
            unique_ips = list(dict.fromkeys(result.ip_addresses))

            # Convert Unix timestamp into a readable date and time.
            modified_time = datetime.fromtimestamp(
                evidence.modified_time,
                tz=timezone.utc,
            ).strftime("%Y-%m-%d %H:%M:%S UTC")

            writer.writerow([
                evidence.name,
                evidence.extension,
                result.risk_level,
                result.risk_score,
                events.get("failed_login", 0),
                events.get("warning", 0),
                events.get("error", 0),
                events.get("critical", 0),
                events.get("denied", 0),
                "; ".join(unique_ips) if unique_ips else "None",
                evidence.size_bytes,
                modified_time,
                evidence.sha256,
                evidence.path,
                "; ".join(result.reasons) if result.reasons else "None",
            ])


def save_json_summary(
    summary: dict,
    output_path: str
) -> None:
    """Save triage summary information to a JSON file."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)