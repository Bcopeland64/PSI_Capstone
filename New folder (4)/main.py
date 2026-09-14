
import sys
from models import Expense
from data_handler import DataHandler


class ExpenseTrackerApp:
    """Main application controller."""

    def __init__(self):
        self.handler = DataHandler()
        self.expenses = self.handler.load_expenses()

    def run(self) -> None:
        """Main execution loop."""
        while True:
            self._print_menu()
            choice = input("\nSelect an option (1-5): ").strip()

            if choice == "1":
                self._add_expense()
            elif choice == "2":
                self._view_expenses()
            elif choice == "3":
                self._show_summary()
            elif choice == "4":
                self._delete_expense()
            elif choice == "5":
                print("\nData saved. Goodbye!")
                self.handler.save_expenses(self.expenses)
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def _print_menu(self) -> None:
        print("\n" + "=" * 35)
        print("   PERSONAL EXPENSE TRACKER   ")
        print("=" * 35)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Financial Summary")
        print("4. Delete Expense")
        print("5. Save & Exit")

    def _add_expense(self) -> None:
        print("\n--- Add New Expense ---")
        title = input("Description/Title: ").strip()

        while True:
            try:
                amount = float(input("Amount ($): ").strip())
                if amount > 0:
                    break
                print("Amount must be greater than zero.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        category = input("Category (e.g., Food, Transport, Bills): ").strip().capitalize()

        exp_id = f"EXP-{len(self.expenses) + 1:03d}"
        new_expense = Expense(expense_id=exp_id, title=title, amount=amount, category=category)

        self.expenses.append(new_expense)
        self.handler.save_expenses(self.expenses)
        print(f"Expense added successfully! [ID: {exp_id}]")

    def _view_expenses(self) -> None:
        print("\n--- All Recorded Expenses ---")
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        fmt = "{:<8} | {:<18} | {:<10} | {:<12} | {:<10}"
        print(fmt.format("ID", "Title", "Amount", "Category", "Date"))
        print("-" * 68)
        for e in self.expenses:
            print(fmt.format(e.expense_id, e.title[:16], f"${e.amount:.2f}", e.category, e.date))

        def _show_summary(self) -> None:
            print("\n--- Financial Summary ---")
            if not self.expenses:
                print("No data available for summary.")
                return

            total = sum(e.amount for e in self.expenses)
            print(f"Total Expenditure: ${total:.2f}")

            categories = {}
            for e in self.expenses:
                categories[e.category] = categories.get(e.category, 0.0) + e.amount

            print("\nBreakdown by Category:")
            for cat, amt in categories.items():
                percentage = (amt / total) * 100
                print(f" - {cat}: ${amt:.2f} ({percentage:.1f}%)")

    def _delete_expense(self) -> None:
        exp_id = input("\nEnter Expense ID to delete (e.g., EXP-001): ").strip().upper()
        target = next((e for e in self.expenses if e.expense_id == exp_id), None)

        if not target:
            print("Expense ID not found.")
            return

        self.expenses.remove(target)
        self.handler.save_expenses(self.expenses)
        print(f"Expense {exp_id} removed successfully.")


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()