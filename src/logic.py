from __future__ import annotations

from pathlib import Path
from typing import Any

from .data_handler import append_transaction_csv, read_inventory_csv, read_transactions_csv, write_inventory_csv
from .models import InventoryItem, Transaction
from .utils import ensure_directory, safe_float, safe_int, validate_non_empty

class InventoryManager:
    def __init__(self, data_dir: str | Path):
        self.data_dir = ensure_directory(data_dir)
        self.inventory_file = self.data_dir / "inventory.csv"
        self.transactions_file = self.data_dir / "transactions.csv"
        self.items: dict[str, InventoryItem] = {}
        self.transactions: list[Transaction] = []
        self.load()

    def load(self) -> None:
        self.items = {}
        loaded_items = read_inventory_csv(self.inventory_file)
        for item in loaded_items:
            self.items[item.sku] = item

        self.transactions = read_transactions_csv(self.transactions_file)

    def save(self) -> None:
        write_inventory_csv(self.inventory_file, self.items.values())
        # transactions are appended as they occur, so no full rewrite required
        # but this keeps the state consistent in memory for any future logic.
        # A full rewrite could also be implemented if needed.

    def add_item(self, item: InventoryItem) -> InventoryItem:
        if item.sku in self.items:
            raise ValueError(f"Item with SKU '{item.sku}' already exists.")
        self.items[item.sku] = item
        self.save()
        return item

    def find_item(self, sku: str) -> InventoryItem | None:
        return self.items.get(sku.strip())

    def update_stock(self, sku: str, delta: int, note: str = "Manual adjustment") -> InventoryItem:
        item = self.find_item(sku)
        if item is None:
            raise ValueError(f"Item with SKU '{sku}' was not found.")

        original_quantity = item.quantity
        item.adjust_quantity(delta)
        transaction = Transaction(
            transaction_id=f"TXN-{len(self.transactions) + 1:05d}",
            sku=item.sku,
            action="IN" if delta >= 0 else "OUT",
            quantity=abs(delta),
            note=note,
        )
        self.transactions.append(transaction)
        append_transaction_csv(self.transactions_file, transaction)
        self.save()
        if item.quantity != original_quantity:
            item.last_updated = transaction.created_at
        return item

    def list_all_items(self) -> list[InventoryItem]:
        return sorted(self.items.values(), key=lambda item: item.name.lower())

    def list_low_stock(self) -> list[InventoryItem]:
        return [item for item in self.list_all_items() if item.is_low_stock()]

    def generate_report(self) -> dict[str, Any]:
        total_value = sum(item.quantity * item.price for item in self.items.values())
        low_stock = self.list_low_stock()
        return {
            "total_items": len(self.items),
            "total_inventory_value": total_value,
            "low_stock_count": len(low_stock),
            "low_stock_items": [item.sku for item in low_stock],
        }

    def remove_item(self, sku: str) -> InventoryItem:
        item = self.find_item(sku)
        if item is None:
            raise ValueError(f"Item with SKU '{sku}' not found.")
        del self.items[sku]
        self.save()
        return item

    def search_items(self, keyword: str) -> list[InventoryItem]:
        query = keyword.strip().lower()
        if not query:
            return self.list_all_items()
        return [
            item
            for item in self.list_all_items()
            if query in item.name.lower() or query in item.sku.lower() or query in item.category.lower()
        ]