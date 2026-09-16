"""Input/output operations for logs and reports."""

import json
import os

import pandas as pd


def read_log_file(file_path: str) -> list[str]:
    """Read non-empty lines from a text log file."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return [line.strip() for line in file if line.strip()]


def save_json(data: dict, output_path: str) -> None:
    """Persist a dictionary as formatted JSON."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_events_csv(events: list[dict], output_path: str) -> None:
    """Persist parsed events to CSV using Pandas."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    dataframe = pd.DataFrame(events)
    dataframe.to_csv(output_path, index=False)


def save_summary_csv(result: dict, output_path: str) -> None:
    """Save high-level triage metrics to a CSV file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    summary = pd.DataFrame(
        [
            {"metric": "Total Events", "value": result["total_events"]},
            {"metric": "Failed Logins", "value": result["failed_logins"]},
            {
                "metric": "Successful Logins",
                "value": result["successful_logins"],
            },
            {"metric": "Other Events", "value": result["other_events"]},
            {"metric": "Unique IPs", "value": result["unique_ips"]},
            {
                "metric": "Suspicious Events",
                "value": result["suspicious_event_count"],
            },
        ]
    )
    summary.to_csv(output_path, index=False)
