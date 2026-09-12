"""
Customer class for managing customer data.
"""
from datetime import datetime

class Customer:
    """Represents a library customer."""
    
    def __init__(self, customer_id, name, email, phone):
        """
        Initialize a customer.
        
        Args:
            customer_id (str): Unique customer identifier
            name (str): Customer name
            email (str): Customer email
            phone (str): Customer phone number
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.borrowed_books = []  # List of book IDs currently borrowed
    
    def to_dict(self):
        """Convert customer to dictionary for storage."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'registration_date': self.registration_date
        }
    
    def __repr__(self):
        """String representation of customer."""
        return f"Customer(ID: {self.customer_id}, Name: {self.name}, Email: {self.email})"
