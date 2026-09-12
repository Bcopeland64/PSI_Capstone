"""
Data Handler for reading and writing to CSV files.
"""
import csv
import os
from book import Book
from customer import Customer
from transaction import Transaction


class DataHandler:
    """Handles data persistence (CSV read/write)."""
    
    def __init__(self, data_dir='../data'):
        """Initialize data handler."""
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, 'books.csv')
        self.customers_file = os.path.join(data_dir, 'customers.csv')
        self.transactions_file = os.path.join(data_dir, 'transactions.csv')
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    # ===== SAVE OPERATIONS =====
    
    def save_books(self, books_dict):
        """Save books to CSV."""
        try:
            with open(self.books_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'book_id', 'title', 'author', 'isbn', 'genre',
                    'quantity_available', 'quantity_borrowed', 'quantity_sold'
                ])
                writer.writeheader()
                for book in books_dict.values():
                    writer.writerow(book.to_dict())
            return f"✓ Books saved to {self.books_file}"
        except Exception as e:
            raise Exception(f"Error saving books: {str(e)}")
    
    def save_customers(self, customers_dict):
        """Save customers to CSV."""
        try:
            with open(self.customers_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'customer_id', 'name', 'email', 'phone', 'registration_date'
                ])
                writer.writeheader()
                for customer in customers_dict.values():
                    writer.writerow(customer.to_dict())
            return f"✓ Customers saved to {self.customers_file}"
        except Exception as e:
            raise Exception(f"Error saving customers: {str(e)}")
    
    def save_transactions(self, transactions_dict):
        """Save transactions to CSV."""
        try:
            with open(self.transactions_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'transaction_id', 'book_id', 'customer_id', 'transaction_type',
                    'date', 'due_date', 'returned_date'
                ])
                writer.writeheader()
                for trans in transactions_dict.values():
                    writer.writerow(trans.to_dict())
            return f"✓ Transactions saved to {self.transactions_file}"
        except Exception as e:
            raise Exception(f"Error saving transactions: {str(e)}")
    
    # ===== LOAD OPERATIONS =====
    
    def load_books(self):
        """Load books from CSV."""
        books_dict = {}
        if not os.path.exists(self.books_file):
            return books_dict
        
        try:
            with open(self.books_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(
                        row['book_id'],
                        row['title'],
                        row['author'],
                        row['isbn'],
                        row['genre'],
                        int(row['quantity_available'])
                    )
                    book.quantity_borrowed = int(row['quantity_borrowed'])
                    book.quantity_sold = int(row['quantity_sold'])
                    books_dict[book.book_id] = book
            return books_dict
        except Exception as e:
            raise Exception(f"Error loading books: {str(e)}")
    
    def load_customers(self):
        """Load customers from CSV."""
        customers_dict = {}
        if not os.path.exists(self.customers_file):
            return customers_dict
        
        try:
            with open(self.customers_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customer = Customer(
                        row['customer_id'],
                        row['name'],
                        row['email'],
                        row['phone']
                    )
                    customer.registration_date = row['registration_date']
                    customers_dict[customer.customer_id] = customer
            return customers_dict
        except Exception as e:
            raise Exception(f"Error loading customers: {str(e)}")
    
    def load_transactions(self):
        """Load transactions from CSV."""
        transactions_dict = {}
        if not os.path.exists(self.transactions_file):
            return transactions_dict
        
        try:
            with open(self.transactions_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trans = Transaction(
                        row['transaction_id'],
                        row['book_id'],
                        row['customer_id'],
                        row['transaction_type'],
                        row['due_date']
                    )
                    trans.date = row['date']
                    trans.returned_date = row['returned_date']
                    transactions_dict[trans.transaction_id] = trans
            return transactions_dict
        except Exception as e:
            raise Exception(f"Error loading transactions: {str(e)}")

