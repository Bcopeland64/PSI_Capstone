import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "incidents.json")


def load_incidents():
    """
    Load incidents from JSON file.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_incidents(incidents):
    """
    Save incidents to JSON file.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(incidents, file, indent=4)