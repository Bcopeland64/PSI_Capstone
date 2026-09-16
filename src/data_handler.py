"""CSV persistence for tasks."""
import csv
import os
from src.models.entities import Task, Priority

FIELDNAMES = ["id", "title", "priority", "done", "created_at"]


def save_tasks(tasks, path):
    """Write tasks to a CSV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for t in tasks:
            writer.writerow(t.to_dict())


def load_tasks(path):
    """Load tasks from CSV. Returns [] if file missing."""
    if not os.path.exists(path):
        return []
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                tasks.append(Task(
                    id=int(row["id"]),
                    title=row["title"],
                    priority=Priority(row.get("priority", "medium")),
                    done=row.get("done", "false").lower() == "true",
                    created_at=row.get("created_at", ""),
                ))
            except (ValueError, KeyError):
                continue  # skip malformed rows
    return tasks
