import json
import os
import pandas as pd
from utils import ensure_data_folder

class Item:
    """Represents an individual inventory item."""
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

class InventoryManager:
    """Manages inventory operations, file persistence, and reporting."""
    def __init__(self, filepath="data/inventory.json"):
        self.filepath = filepath
        self.items = {}
        self.history = []
        ensure_data_folder(self.filepath)
        self.load_data()

    def add_item(self, item_id, name, quantity, price):
        if item_id in self.items:
            print(f"Error: Item ID {item_id} already exists.")
            return False

        new_item = Item(item_id, name, quantity, price)
        self.items[item_id] = new_item
        self._log_transaction(item_id, "ADD", quantity)
        self.save_data()
        print(f"Item '{name}' added successfully.")
        return True

    def update_stock(self, item_id, change_qty):
        if item_id not in self.items:
            print("Error: Item ID not found.")
            return False

        item = self.items[item_id]
        if item.quantity + change_qty < 0:
            print("Error: Stock cannot go below zero.")
            return False

        item.quantity += change_qty
        action = "RESTOCK" if change_qty > 0 else "REMOVE_STOCK"
        self._log_transaction(item_id, action, abs(change_qty))
        self.save_data()
        print(f"Stock updated. New quantity: {item.quantity}")
        return True

    def _log_transaction(self, item_id, action, qty):
        self.history.append({
            "item_id": item_id,
            "action": action,
            "quantity": qty
        })

    def display_report(self):
        if not self.items:
            print("Inventory is currently empty.")
            return

        data = [item.to_dict() for item in self.items.values()]
        df = pd.DataFrame(data)
        df["total_value"] = df["quantity"] * df["price"]
        
        print("\n--- INVENTORY REPORT ---")
        print(df.to_string(index=False))
        print(f"Total Inventory Value: ${df['total_value'].sum():.2f}\n")

    def display_history(self):
        if not self.history:
            print("No transaction history available.")
            return

        df = pd.DataFrame(self.history)
        print("\n--- TRANSACTION HISTORY ---")
        print(df.to_string(index=False))
        print()

    def save_data(self):
        data = {
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "history": self.history
        }
        try:
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                
                for item_id, info in data.get("items", {}).items():
                    self.items[item_id] = Item(
                        info["item_id"], 
                        info["name"], 
                        info["quantity"], 
                        info["price"]
                    )
                self.history = data.get("history", [])
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading saved data: {e}")
