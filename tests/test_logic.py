"""
Extra credit unit tests for my classes.
"""
import unittest
import os
from src.logic import MyBook, LibraryManager

class TestMyCode(unittest.TestCase):
    def setUp(self):
        """Runs before every test. Creates a fake file name."""
        self.fake_file = "fake_test_data.csv"
        self.test_manager = LibraryManager(self.fake_file)

    def tearDown(self):
        """Runs after every test to clean up the fake file."""
        if os.path.exists(self.fake_file):
            os.remove(self.fake_file)

    def test_mybook_class_works(self):
        """Tests if the book object saves variables correctly."""
        test_book = MyBook("Harry Potter", "J.K. Rowling", "1997")
        self.assertEqual(test_book.title, "Harry Potter")
        self.assertEqual(test_book.author, "J.K. Rowling")
        
    def test_saving_and_loading(self):
        """Tests if saving to CSV and reading back works."""
        book = MyBook("The Hobbit", "J.R.R. Tolkien", "1937")
        self.test_manager.list_of_books.append(book)
        self.test_manager.save_books_to_csv()
        
        # Make a second manager to see if it reads the file we just made
        manager2 = LibraryManager(self.fake_file)
        self.assertEqual(len(manager2.list_of_books), 1)
        self.assertEqual(manager2.list_of_books[0].title, "The Hobbit")

if __name__ == "__main__":
    unittest.main()