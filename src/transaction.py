"""
Transaction class for logging book borrowing, returns, and sales.
"""
from datetime import datetime, timedelta

class Transaction:
    """Represents a transaction (borrow, return, or sale)."""
    
    def __init__(self, transaction_id, book_id, customer_id, transaction_type, due_date=None):
        """
        Initialize a transaction.
        
        Args:
            transaction_id (str): Unique transaction ID
            book_id (str): ID of the book
            customer_id (str): ID of the customer
            transaction_type (str): 'borrow', 'return', or 'sell'
            due_date (str): Due date for borrowed books (auto-calculated if None)
        """
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.customer_id = customer_id
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Auto-calculate due date (14 days from now for borrows)
        if transaction_type == 'borrow' and due_date is None:
            due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        self.due_date = due_date
        self.returned_date = None
    
    def mark_returned(self):
        """Mark the book as returned."""
        self.returned_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transaction_type = 'return'
    
    def to_dict(self):
        """Convert transaction to dictionary for storage."""
        return {
            'transaction_id': self.transaction_id,
            'book_id': self.book_id,
            'customer_id': self.customer_id,
            'transaction_type': self.transaction_type,
            'date': self.date,
            'due_date': self.due_date,
            'returned_date': self.returned_date
        }
    
    def __repr__(self):
        """String representation of transaction."""
        return f"Transaction(ID: {self.transaction_id}, Book: {self.book_id}, Type: {self.transaction_type})"
