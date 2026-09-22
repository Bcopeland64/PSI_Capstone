from __future__ import annotations

import pytest

from src.logic import InventoryManager
from src.models import InventoryItem


def test_add_item_and_update_stock(tmp_path):
    manager = InventoryManager(tmp_path)

    item = InventoryItem(
        sku="SKU-100",
        name="Notebook",
        category="Office",
        quantity=10,
        price=3.5,
        reorder_level=3,
    )
    manager.add_item(item)

    assert manager.find_item("SKU-100").name == "Notebook"

    manager.update_stock("SKU-100", -5, note="Sold 5 notebooks")
    assert manager.find_item("SKU-100").quantity == 5

    manager.update_stock("SKU-100", 7, note="Restocked")
    assert manager.find_item("SKU-100").quantity == 12


def test_low_stock_detection(tmp_path):
    manager = InventoryManager(tmp_path)

    manager.add_item(
        InventoryItem(
            sku="SKU-200",
            name="Marker",
            category="School",
            quantity=2,
            price=1.25,
            reorder_level=5,
        )
    )

    low_stock = manager.list_low_stock()
    assert len(low_stock) == 1
    assert low_stock[0].sku == "SKU-200"


def test_negative_quantity_not_allowed(tmp_path):
    manager = InventoryManager(tmp_path)

    with pytest.raises(ValueError):
        manager.add_item(
            InventoryItem(
                sku="SKU-300",
                name="Invalid Product",
                category="Test",
                quantity=-1,
                price=10.0,
            )
        )