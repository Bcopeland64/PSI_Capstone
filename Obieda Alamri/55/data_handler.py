"""
data_handler.py
Handles JSON and CSV data persistence, file creation, and exception handling.
"""

import json
import csv
import os
from typing import List, Dict


class DataHandler:
    """Manages file storage and data retrieval."""

    def __init__(self, json_filepath: str = "data/incidents.json"):
        self.json_filepath = json_filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the data directory and default file if non-existent."""
        os.makedirs(os.path.dirname(self.json_filepath), exist_ok=True)
        if not os.path.exists(self.json_filepath):
            with open(self.json_filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save_incidents(self, incidents_data: List[Dict]) -> bool:
        """Saves a list of incident dictionaries to JSON file."""
        try:
            with open(self.json_filepath, 'w', encoding='utf-8') as f:
                json.dump(incidents_data, f, indent=4)
            return True
        except IOError as e:
            print(f"[Error] Failed to write to file: {e}")
            return False

    def load_incidents(self) -> List[Dict]:
        """Loads incident data from JSON file with error handling."""
        try:
            with open(self.json_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[Warning] Issue loading data ({e}). Returning empty list.")
            return []

    def export_to_csv(self, csv_filepath: str = "data/export_report.csv") -> bool:
        """Exports JSON data to CSV for external reporting."""
        data = self.load_incidents()
        if not data:
            print("[Info] No data available to export.")
            return False

        try:
            fieldnames = ["incident_id", "title", "severity", "timestamp", "type", "ip_address"]
            with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    # Fill missing keys if any
                    row_data = {field: row.get(field, "N/A") for field in fieldnames}
                    writer.writerow(row_data)
            print(f"[Success] Data exported to {csv_filepath}")
            return True
        except Exception as e:
            print(f"[Error] Failed to export CSV: {e}")
            return False