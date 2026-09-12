"""
This is the main file that runs the program. Run this file!
"""
import sys
import os
from src.logic import LibraryManager
from src.utils import get_user_input_safely

def start_program():
    """
    Starts the main menu loop for the user.
    """
    # Find out where we are
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    csv_path = os.path.join(parent_folder, 'data', 'sample_data.csv')
    
    # Initialize my library manager class
    my_manager = LibraryManager(csv_path)
    
    print("Hello! Welcome to my Library App.")
    
    # Main program loop
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Search for a book to add")
        print("2. See all my saved books")
        print("3. Quit program")
        
        user_choice = get_user_input_safely("Please type 1, 2, or 3: ", ["1", "2", "3"])
        
        if user_choice == '1':
            search_word = get_user_input_safely("Enter a book name or author to search: ", [])
            my_manager.search_and_add_book(search_word)
                
        elif user_choice == '2':
            my_manager.show_all_books()
            
        elif user_choice == '3':
            print("Thanks for using my app.")
            sys.exit(0)

if __name__ == "__main__":
    start_program()