import sys
from logic import InventoryManager
from utils import validate_positive_int, validate_positive_float

def main():
    manager = InventoryManager()

    while True:
        print("=== INVENTORY MANAGEMENT SYSTEM ===")
        print("1. Add New Item")
        print("2. Restock Item")
        print("3. Remove Stock")
        print("4. View Inventory Report")
        print("5. View Transaction History")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            item_id = input("Enter Item ID: ").strip()
            name = input("Enter Item Name: ").strip()
            qty = validate_positive_int("Enter Initial Quantity: ")
            price = validate_positive_float("Enter Unit Price: ")
            manager.add_item(item_id, name, qty, price)

        elif choice == "2":
            item_id = input("Enter Item ID to restock: ").strip()
            qty = validate_positive_int("Enter quantity to add: ")
            manager.update_stock(item_id, qty)

        elif choice == "3":
            item_id = input("Enter Item ID to remove stock from: ").strip()
            qty = validate_positive_int("Enter quantity to remove: ")
            manager.update_stock(item_id, -qty)

        elif choice == "4":
            manager.display_report()

        elif choice == "5":
            manager.display_history()

        elif choice == "6":
            print("Exiting system. Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Please select numbers 1-6.\n")

if __name__ == "__main__":
    main()
