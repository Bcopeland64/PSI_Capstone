"""
Library Manager class for handling library operations.
"""
from book import Book
from customer import Customer
from transaction import Transaction
from datetime import datetime

class LibraryManager:
    """Manages the library's books, customers, and transactions."""
    
    def __init__(self):
        """Initialize the library manager."""
        self.books = {}  # {book_id: Book object}
        self.customers = {}  # {customer_id: Customer object}
        self.transactions = {}  # {transaction_id: Transaction object}
        self.transaction_counter = 0
    
    # ===== BOOK OPERATIONS =====
    
    def add_book(self, book_id, title, author, isbn, genre, quantity=1):
        """Add a new book to the library."""
        if book_id in self.books:
            raise ValueError(f"Book ID {book_id} already exists!")
        
        book = Book(book_id, title, author, isbn, genre, quantity)
        self.books[book_id] = book
        return f"✓ Book '{title}' added successfully!"
    
    def get_book(self, book_id):
        """Get a book by ID."""
        if book_id not in self.books:
            raise ValueError(f"Book ID {book_id} not found!")
        return self.books[book_id]
    
    def list_books(self):
        """List all books."""
        if not self.books:
            return "No books in the library."
        return self.books
    
    def update_book_quantity(self, book_id, new_quantity):
        """Update available quantity of a book."""
        book = self.get_book(book_id)
        book.quantity_available = new_quantity
        return f"✓ Updated {book.title} quantity to {new_quantity}"
    
    # ===== CUSTOMER OPERATIONS =====
    
    def add_customer(self, customer_id, name, email, phone):
        """Add a new customer."""
        if customer_id in self.customers:
            raise ValueError(f"Customer ID {customer_id} already exists!")
        
        customer = Customer(customer_id, name, email, phone)
        self.customers[customer_id] = customer
        return f"✓ Customer '{name}' registered successfully!"
    
    def get_customer(self, customer_id):
        """Get a customer by ID."""
        if customer_id not in self.customers:
            raise ValueError(f"Customer ID {customer_id} not found!")
        return self.customers[customer_id]
    
    def list_customers(self):
        """List all customers."""
        if not self.customers:
            return "No customers registered."
        return self.customers
    
    # ===== TRANSACTION OPERATIONS =====
    
    def borrow_book(self, book_id, customer_id):
        """Record a book borrow transaction."""
        book = self.get_book(book_id)
        customer = self.get_customer(customer_id)
        
        if book.quantity_available <= 0:
            raise ValueError(f"'{book.title}' is not available!")
        
        self.transaction_counter += 1
        trans_id = f"T{self.transaction_counter:05d}"
        
        transaction = Transaction(trans_id, book_id, customer_id, 'borrow')
        self.transactions[trans_id] = transaction
        
        # Update quantities
        book.quantity_available -= 1
        book.quantity_borrowed += 1
        customer.borrowed_books.append(book_id)
        
        return f"✓ Book '{book.title}' borrowed by {customer.name}. Due: {transaction.due_date}"
    
    def return_book(self, book_id, customer_id):
        """Record a book return transaction."""
        book = self.get_book(book_id)
        customer = self.get_customer(customer_id)
        
        # Find the borrow transaction
        borrow_trans = None
        for trans in self.transactions.values():
            if (trans.book_id == book_id and 
                trans.customer_id == customer_id and 
                trans.transaction_type == 'borrow' and 
                trans.returned_date is None):
                borrow_trans = trans
                break
        
        if not borrow_trans:
            raise ValueError(f"No active borrow record found!")
        
        borrow_trans.mark_returned()
        
        # Update quantities
        book.quantity_available += 1
        book.quantity_borrowed -= 1
        if book_id in customer.borrowed_books:
            customer.borrowed_books.remove(book_id)
        
        return f"✓ Book '{book.title}' returned by {customer.name}"
    
    def sell_book(self, book_id, quantity=1):
        """Record a book sale."""
        book = self.get_book(book_id)
        
        if book.quantity_available < quantity:
            raise ValueError(f"Insufficient stock! Available: {book.quantity_available}")
        
        self.transaction_counter += 1
        trans_id = f"T{self.transaction_counter:05d}"
        
        transaction = Transaction(trans_id, book_id, "SALE", 'sell')
        self.transactions[trans_id] = transaction
        
        # Update quantities
        book.quantity_available -= quantity
        book.quantity_sold += quantity
        
        return f"✓ Sold {quantity} copy(ies) of '{book.title}'"
    
    # ===== REPORTS =====
    
    def get_overdue_books(self):
        """Get all overdue borrowed books."""
        overdue = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for trans in self.transactions.values():
            if (trans.transaction_type == 'borrow' and 
                trans.returned_date is None and 
                trans.due_date < today):
                overdue.append({
                    'transaction_id': trans.transaction_id,
                    'book_id': trans.book_id,
                    'customer_id': trans.customer_id,
                    'due_date': trans.due_date
                })
        
        return overdue
    
    def get_customer_borrowed_books(self, customer_id):
        """Get all books currently borrowed by a customer."""
        customer = self.get_customer(customer_id)
        borrowed = []
        
        for trans in self.transactions.values():
            if (trans.customer_id == customer_id and 
                trans.transaction_type == 'borrow' and 
                trans.returned_date is None):
                borrowed.append({
                    'transaction_id': trans.transaction_id,
                    'book_title': self.books[trans.book_id].title,
                    'due_date': trans.due_date
                })
        
        return borrowed
    
    def get_low_stock_books(self, threshold=3):
        """Get books with low available quantity."""
        low_stock = []
        for book in self.books.values():
            if book.quantity_available < threshold:
                low_stock.append(book.to_dict())
        return low_stock
    
    def get_sold_books_report(self):
        """Get report of all sold books."""
        sold = []
        for trans in self.transactions.values():
            if trans.transaction_type == 'sell':
                sold.append({
                    'transaction_id': trans.transaction_id,
                    'book_title': self.books[trans.book_id].title,
                    'date': trans.date
                })
        return sold
