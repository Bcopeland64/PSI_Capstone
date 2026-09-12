"""
Book class for managing book data.
"""

class Book:
    """Represents a book in the library."""
    
    def __init__(self, book_id, title, author, isbn, genre, quantity_available=1):
        """
        Initialize a book.
        
        Args:
            book_id (str): Unique book identifier
            title (str): Book title
            author (str): Author name
            isbn (str): ISBN number
            genre (str): Genre category
            quantity_available (int): Available copies
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.quantity_available = quantity_available
        self.quantity_borrowed = 0
        self.quantity_sold = 0
    
    def to_dict(self):
        """Convert book to dictionary for storage."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'quantity_available': self.quantity_available,
            'quantity_borrowed': self.quantity_borrowed,
            'quantity_sold': self.quantity_sold
        }
    
    def __repr__(self):
        """String representation of book."""
        return f"Book(ID: {self.book_id}, Title: {self.title}, Available: {self.quantity_available})"
