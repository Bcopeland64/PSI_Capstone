from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .models import InventoryItem, Transaction


def read_inventory_csv(path: Path) -> list[InventoryItem]:
    if not path.exists():
        return []

    items: list[InventoryItem] = []
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                item = InventoryItem(
                    sku=row.get("sku", "").strip(),
                    name=row.get("name", "").strip(),
                    category=row.get("category", "").strip(),
                    quantity=int(row.get("quantity", 0)),
                    price=float(row.get("price", 0.0)),
                    reorder_level=int(row.get("reorder_level", 5)),
                    description=row.get("description", ""),
                    last_updated=row.get("last_updated", ""),
                )
                items.append(item)
            except (TypeError, ValueError):
                continue

    return items


def write_inventory_csv(path: Path, items: Iterable[InventoryItem]) -> None:
    fieldnames = [
        "sku",
        "name",
        "category",
        "quantity",
        "price",
        "reorder_level",
        "description",
        "last_updated",
    ]
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item.to_dict())


def read_transactions_csv(path: Path) -> list[Transaction]:
    if not path.exists():
        return []

    transactions: list[Transaction] = []
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                transaction = Transaction(
                    transaction_id=row.get("transaction_id", "").strip(),
                    sku=row.get("sku", "").strip(),
                    action=row.get("action", "").strip(),
                    quantity=int(row.get("quantity", 0)),
                    created_at=row.get("created_at", ""),
                    note=row.get("note", ""),
                )
                transactions.append(transaction)
            except (TypeError, ValueError):
                continue

    return transactions


def append_transaction_csv(path: Path, transaction: Transaction) -> None:
    fieldnames = [
        "transaction_id",
        "sku",
        "action",
        "quantity",
        "created_at",
        "note",
    ]
    file_exists = path.exists()

    with path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "transaction_id": transaction.transaction_id,
                "sku": transaction.sku,
                "action": transaction.action,
                "quantity": transaction.quantity,
                "created_at": transaction.created_at,
                "note": transaction.note,
            }
        )