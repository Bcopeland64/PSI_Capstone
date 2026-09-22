from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Transaction:
    transaction_id: str
    sku: str
    action: str
    quantity: int
    created_at: str = field(default_factory=current_timestamp)
    note: str = ""

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("Transaction ID cannot be empty.")
        if not self.sku.strip():
            raise ValueError("SKU cannot be empty.")
        if self.action not in {"IN", "OUT", "ADJUST"}:
            raise ValueError("Action must be one of: IN, OUT, ADJUST.")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if not self.created_at:
            self.created_at = current_timestamp()


@dataclass
class InventoryItem:
    sku: str
    name: str
    category: str
    quantity: int
    price: float
    reorder_level: int = 5
    description: str = ""
    last_updated: str = field(default_factory=current_timestamp)

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("SKU cannot be empty.")
        if not self.name.strip():
            raise ValueError("Item name cannot be empty.")
        if not self.category.strip():
            raise ValueError("Category cannot be empty.")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        if self.reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")
        if not self.last_updated:
            self.last_updated = current_timestamp()

    def is_low_stock(self) -> bool:
        return self.quantity <= self.reorder_level

    def adjust_quantity(self, delta: int) -> int:
        new_quantity = self.quantity + delta
        if new_quantity < 0:
            raise ValueError(f"Cannot reduce {self.name} below zero stock.")
        self.quantity = new_quantity
        self.last_updated = current_timestamp()
        return self.quantity

    def to_dict(self) -> dict[str, Any]:
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "reorder_level": self.reorder_level,
            "description": self.description,
            "last_updated": self.last_updated,
        }