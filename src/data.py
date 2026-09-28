import json
import os


DATA_FILE = "tasks.json"


def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

    except OSError as error:
        print(f"Error saving tasks: {error}")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        print("Could not load saved tasks.")
        return []