"""
This file contains the classes for my books and the library manager.
"""
import csv
import os
from src.utils import get_data_from_google_api

class MyBook:
    """
    This class represents a single book in the library.
    """
    def __init__(self, book_title, book_author, book_year):
        # Set the attributes for the book object
        self.title = book_title
        self.author = book_author
        self.year = book_year

    def convert_to_dictionary(self):
        """
        Returns a dictionary so we can save it to the CSV file easily.
        """
        my_dict = {
            "Title": self.title, 
            "Author": self.author, 
            "Year": self.year
        }
        return my_dict

class LibraryManager:
    """
    This class manages the list of books and does the file saving/loading.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.list_of_books = []
        # Load books as soon as we start the program
        self.read_books_from_csv()

    def read_books_from_csv(self):
        """
        Reads the CSV file and creates MyBook objects.
        """
        if os.path.exists(self.file_path) == False:
            # If file doesn't exist yet, just exit the function
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    # Get the data from each column
                    title = row.get('Title', 'Unknown')
                    author = row.get('Author', 'Unknown')
                    year = row.get('Year', 'Unknown')
                    
                    # Create a book object and add it to my list
                    book_obj = MyBook(title, author, year)
                    self.list_of_books.append(book_obj)
        except Exception as e:
            print(f"We could not read the file. Error: {e}")

    def save_books_to_csv(self):
        """
        Saves all books in our list back into the CSV file.
        """
        try:
            # Make sure the data folder exists first
            folder_path = os.path.dirname(self.file_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                columns = ['Title', 'Author', 'Year']
                csv_writer = csv.DictWriter(f, fieldnames=columns)
                
                csv_writer.writeheader()
                # Loop through my books and write them out
                for book in self.list_of_books:
                    csv_writer.writerow(book.convert_to_dictionary())
        except Exception as e:
            print(f"Could not save to the file. Error: {e}")

    def search_and_add_book(self, search_term):
        """
        Searches the Google API and adds the first book it finds.
        """
        print(f"Looking up '{search_term}' on Google Books...")
        api_result = get_data_from_google_api(search_term)
        
        if api_result != None and "items" in api_result:
            first_book = api_result["items"][0]["volumeInfo"]
            
            # Get book details using .get() just in case they are missing from Google
            book_title = first_book.get("title", "No Title Found")
            
            authors_list = first_book.get("authors", ["No Author"])
            book_author = authors_list[0] # Just grab the first author
            
            published_date = first_book.get("publishedDate", "0000")
            book_year = published_date[0:4] # Get the first 4 characters for the year
            
            # Create new book and add it to our list
            new_book = MyBook(book_title, book_author, book_year)
            self.list_of_books.append(new_book)
            
            # Save the changes to the file right away
            self.save_books_to_csv()
            
            print(f"Yay! Added '{book_title}' to your library.")
        else:
            print("Sorry, I couldn't find any books matching that search.")

    def show_all_books(self):
        """
        Prints out all the books currently saved in the library list.
        """
        if len(self.list_of_books) == 0:
            print("You have no books in your library yet.")
        else:
            print("\n=== My Book Library ===")
            index = 1
            for book in self.list_of_books:
                print(f"{index}. {book.title} by {book.author} (Published: {book.year})")
                index = index + 1
            print("=======================\n")