
import json
import os
from typing import List
from models import Expense


class DataHandler:
    """Manages loading and saving expense data to local storage."""

    def __init__(self, filepath: str = "data/expenses.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensures the target directory and JSON file exist."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_expenses(self) -> List[Expense]:
        """Loads all expenses from the JSON file."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, Exception):
            return []

    def save_expenses(self, expenses: List[Expense]) -> bool:
        """Saves a list of Expense objects to the JSON file."""
        try:
            serialized = [e.to_dict() for e in expenses]
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False