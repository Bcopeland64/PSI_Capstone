from __future__ import annotations

import sys
from pathlib import Path

from .logic import InventoryManager
from .models import InventoryItem
from .utils import format_currency, safe_float, safe_int, validate_non_empty

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
except ImportError:
    Console = None
    def rprint(*args, **kwargs):  # type: ignore[no-redef]
        print(*args)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def build_manager() -> InventoryManager:
    return InventoryManager(DATA_DIR)


def print_items(items: list[InventoryItem]) -> None:
    if not items:
        print("No items available.")
        return

    if Console:
        table = Table(title="Inventory Items")
        table.add_column("SKU")
        table.add_column("Name")
        table.add_column("Category")
        table.add_column("Qty")
        table.add_column("Price")
        table.add_column("Low Stock")
        for item in items:
            table.add_row(
                item.sku,
                item.name,
                item.category,
                str(item.quantity),
                format_currency(item.price),
                "Yes" if item.is_low_stock() else "No",
            )
        Console().print(table)
    else:
        print("\nInventory Items")
        print("-" * 90)
        print(f"{'SKU':<12} {'Name':<20} {'Category':<12} {'Qty':>5} {'Price':>10} {'Low Stock':>10}")
        for item in items:
            print(f"{item.sku:<12} {item.name:<20} {item.category:<12} {item.quantity:>5} {format_currency(item.price):>10} {('Yes' if item.is_low_stock() else 'No'):>10}")
        print("-" * 90)


def add_item_flow(manager: InventoryManager) -> None:
    try:
        sku = validate_non_empty(input("Enter SKU: "), "SKU")
        name = validate_non_empty(input("Enter item name: "), "Name")
        category = validate_non_empty(input("Enter category: "), "Category")
        quantity = safe_int(input("Enter quantity: "), "Quantity")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        price = safe_float(input("Enter unit price: "), "Price")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        reorder_level = safe_int(input("Enter reorder level (default 5): ") or "5", "Reorder level")
        if reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")
        description = input("Enter description (optional): ").strip()

        item = InventoryItem(
            sku=sku,
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            reorder_level=reorder_level,
            description=description,
        )

        manager.add_item(item)
        print(f"Added item: {item.name} ({item.sku})")
    except ValueError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


def update_stock_flow(manager: InventoryManager) -> None:
    sku = input("Enter SKU to update: ").strip()
    if not sku:
        print("SKU cannot be empty.")
        return

    item = manager.find_item(sku)
    if item is None:
        print(f"No item found with SKU {sku}.")
        return

    try:
        delta = safe_int(input("Enter quantity change (+ for restock, - for sale): "), "Quantity change")
        manager.update_stock(sku, delta, note="Manual inventory change")
        print(f"Updated stock for {item.name}. Current quantity: {manager.find_item(sku).quantity}")
    except ValueError as exc:
        print(f"Error: {exc}")


def generate_report(manager: InventoryManager) -> None:
    report = manager.generate_report()
    print("\nInventory Summary")
    print("-" * 50)
    print(f"Total items: {report['total_items']}")
    print(f"Inventory value: {format_currency(report['total_inventory_value'])}")
    print(f"Low-stock items: {report['low_stock_count']}")
    if report["low_stock_items"]:
        print(f"SKUs needing restock: {', '.join(report['low_stock_items'])}")
    else:
        print("No items are currently below reorder level.")
    print("-" * 50)


def main() -> None:
    manager = build_manager()
    while True:
        print("\n=== Task & Inventory Management System ===")
        print("1. View all items")
        print("2. Add item")
        print("3. Update stock")
        print("4. View low-stock items")
        print("5. Generate inventory report")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                print_items(manager.list_all_items())
            elif choice == "2":
                add_item_flow(manager)
            elif choice == "3":
                update_stock_flow(manager)
            elif choice == "4":
                print_items(manager.list_low_stock())
            elif choice == "5":
                generate_report(manager)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid selection. Please try again.")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully.")
        sys.exit(0)