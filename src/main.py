# -*- coding: utf-8 -*-

"""
Main CLI application for MyBooks Library Manager.
"""

import sys
import os

# Add the src folder to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from library_manager import LibraryManager
from data_handler import DataHandler


def print_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print(" MYBOOKS - LIBRARY MANAGER ")
    print("="*50)
    print("\n[BOOKS]")
    print("1.  Add a new book")
    print("2.  List all books")
    print("3.  Update book quantity")
    print("\n[CUSTOMERS]")
    print("4.  Register new customer")
    print("5.  List all customers")
    print("\n[TRANSACTIONS]")
    print("6.  Borrow a book")
    print("7.  Return a book")
    print("8.  Sell a book")
    print("\n[REPORTS]")
    print("9.  View customer's borrowed books")
    print("10. View overdue books")
    print("11. View low-stock books")
    print("12. View sales report")
    print("\n[DATA]")
    print("13. Save all data")
    print("14. Load all data")
    print("\n0.  Exit")
    print("="*50)

def add_book(library):
    """Add a new book to the library."""
    try:
        print("\n--- ADD NEW BOOK ---")
        book_id = input("Enter book ID (e.g., B001): ").strip()
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()
        genre = input("Enter genre: ").strip()
        quantity = int(input("Enter quantity available: ").strip())
        
        result = library.add_book(book_id, title, author, isbn, genre, quantity)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def list_books(library):
    """Display all books."""
    books = library.list_books()
    if isinstance(books, str):
        print(f"\n{books}")
    else:
        print("\n--- ALL BOOKS ---")
        for book in books.values():
            print(f"  {book}")

def update_book_quantity(library):
    """Update book quantity."""
    try:
        print("\n--- UPDATE BOOK QUANTITY ---")
        book_id = input("Enter book ID: ").strip()
        new_qty = int(input("Enter new quantity: ").strip())
        result = library.update_book_quantity(book_id, new_qty)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def add_customer(library):
    """Register a new customer."""
    try:
        print("\n--- REGISTER NEW CUSTOMER ---")
        customer_id = input("Enter customer ID (e.g., C001): ").strip()
        name = input("Enter customer name: ").strip()
        email = input("Enter email: ").strip()
        phone = input("Enter phone number: ").strip()
        
        result = library.add_customer(customer_id, name, email, phone)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def list_customers(library):
    """Display all customers."""
    customers = library.list_customers()
    if isinstance(customers, str):
        print(f"\n{customers}")
    else:
        print("\n--- ALL CUSTOMERS ---")
        for customer in customers.values():
            print(f"  {customer}")

def borrow_book(library):
    """Record a book borrow."""
    try:
        print("\n--- BORROW A BOOK ---")
        book_id = input("Enter book ID: ").strip()
        customer_id = input("Enter customer ID: ").strip()
        result = library.borrow_book(book_id, customer_id)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def return_book(library):
    """Record a book return."""
    try:
        print("\n--- RETURN A BOOK ---")
        book_id = input("Enter book ID: ").strip()
        customer_id = input("Enter customer ID: ").strip()
        result = library.return_book(book_id, customer_id)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def sell_book(library):
    """Record a book sale."""
    try:
        print("\n--- SELL A BOOK ---")
        book_id = input("Enter book ID: ").strip()
        quantity = int(input("Enter quantity to sell: ").strip())
        result = library.sell_book(book_id, quantity)
        print(result)
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def view_customer_books(library):
    """View books borrowed by a customer."""
    try:
        print("\n--- CUSTOMER'S BORROWED BOOKS ---")
        customer_id = input("Enter customer ID: ").strip()
        books = library.get_customer_borrowed_books(customer_id)
        
        if not books:
            print("No books currently borrowed.")
        else:
            for book in books:
                print(f"   {book['book_title']} (Due: {book['due_date']})")
    except ValueError as e:
        print(f" Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

def view_overdue_books(library):
    """View overdue books."""
    print("\n--- OVERDUE BOOKS ---")
    overdue = library.get_overdue_books()
    
    if not overdue:
        print("No overdue books.")
    else:
        for book in overdue:
            customer_name = library.get_customer(book['customer_id']).name
            book_title = library.get_book(book['book_id']).title
            print(f"    {book_title} (Customer: {customer_name}, Due: {book['due_date']})")

def view_low_stock(library):
    """View low-stock books."""
    print("\n--- LOW STOCK BOOKS ---")
    low_stock = library.get_low_stock_books()
    
    if not low_stock:
        print("All books have sufficient stock.")
    else:
        for book in low_stock:
            print(f"   {book['title']} (Available: {book['quantity_available']})")

def view_sales_report(library):
    """View sales report."""
    print("\n--- SALES REPORT ---")
    sales = library.get_sold_books_report()
    
    if not sales:
        print("No sales recorded.")
    else:
        for sale in sales:
            print(f"   {sale['book_title']} (Date: {sale['date']})")

def save_data(library, data_handler):
    """Save all data to CSV files."""
    try:
        print("\n--- SAVING DATA ---")
        print(data_handler.save_books(library.books))
        print(data_handler.save_customers(library.customers))
        print(data_handler.save_transactions(library.transactions))
        print("✓ All data saved successfully!")
    except Exception as e:
        print(f" Error saving data: {e}")

def load_data(library, data_handler):
    """Load all data from CSV files."""
    try:
        print("\n--- LOADING DATA ---")
        library.books = data_handler.load_books()
        library.customers = data_handler.load_customers()
        library.transactions = data_handler.load_transactions()
        print("✓ All data loaded successfully!")
    except Exception as e:
        print(f" Error loading data: {e}")

def main():
    """Main application loop."""
    library = LibraryManager()
    data_handler = DataHandler()
    
    print("\n Welcome to MyBooks Library Manager!")
    print("Loading previous data...")
    load_data(library, data_handler)
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (0-14): ").strip()
        
        if choice == '0':
            print("\n Saving data before exit...")
            save_data(library, data_handler)
            print("\n Thank you for using MyBooks! Goodbye!")
            break
        elif choice == '1':
            add_book(library)
        elif choice == '2':
            list_books(library)
        elif choice == '3':
            update_book_quantity(library)
        elif choice == '4':
            add_customer(library)
        elif choice == '5':
            list_customers(library)
        elif choice == '6':
            borrow_book(library)
        elif choice == '7':
            return_book(library)
        elif choice == '8':
            sell_book(library)
        elif choice == '9':
            view_customer_books(library)
        elif choice == '10':
            view_overdue_books(library)
        elif choice == '11':
            view_low_stock(library)
        elif choice == '12':
            view_sales_report(library)
        elif choice == '13':
            save_data(library, data_handler)
        elif choice == '14':
            load_data(library, data_handler)
        else:
            print(" Invalid choice. Please try again.")

if __name__ == "__main__":
    main()