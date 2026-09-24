"""JSON persistence functions."""

import json
from pathlib import Path

try:
    from models import TriageCase
except ImportError:
    from .models import TriageCase

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "triage_cases.json"


def load_cases():
    """Load cases from the JSON data file."""
    try:
        if not DATA_FILE.exists():
            return []

        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [TriageCase.from_dict(item)
                for item in data]
    except (json.JSONDecodeError, OSError, TypeError, KeyError) as error:
        print(f"Warning: Could not load saved cases: {error}")
        return []


def save_cases(cases):
    """Save all cases to the JSON data file."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump([case.to_dict() for case in cases], file, indent=4)
        return True
    except OSError as error:
        print(f"Error saving cases: {error}")
        return False
