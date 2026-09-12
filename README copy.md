
# 📚 MyBooks - Library Management System

A comprehensive command-line library management system that replaces paper-based documentation for tracking borrowed, sold, and managed books.

## 🎯 Features

- **📖 Book Management**: Add, list, and update book inventory
- **👥 Customer Management**: Register customers with unique IDs
- **📤 Borrowing System**: Track book borrowing with automatic 14-day due dates
- **🔄 Return Management**: Record book returns
- **💰 Sales Tracking**: Log book sales and inventory depletion
- **⚠️ Alerts**: View overdue books and low-stock items
- **📊 Reports**: Generate sales reports and customer borrowing history
- **💾 Data Persistence**: Automatic CSV-based data storage and loading

---

## 📋 Technical Requirements Met

✅ **Modular Architecture**: Separate files for models, logic, data handling, and main app
✅ **OOP Design**: Uses classes (Book, Customer, Transaction, LibraryManager)
✅ **Data Persistence**: CSV file storage in `data/` folder
✅ **Error Handling**: Try-except blocks for all user inputs
✅ **Input Validation**: Validates book IDs, customer IDs, quantities
✅ **PEP 8 Compliance**: Clean, readable code with proper naming
✅ **Docstrings**: All classes and functions documented
✅ **Testing**: Unit tests in `tests/` folder
✅ **Repository Structure**: Organized with `src/`, `data/`, `tests/` directories

---

## 📁 Project Structure
MyBooks/
├── src/
│   ├── book.py                 # Book class
│   ├── customer.py             # Customer class
│   ├── transaction.py          # Transaction class
│   ├── library_manager.py      # Main logic and operations
│   ├── data_handler.py         # CSV read/write operations
│   └── main.py                 # CLI menu and user interface
├── data/
│   ├── books.csv              # Stores book data
│   ├── customers.csv          # Stores customer data
│   └── transactions.csv       # Stores transaction history
├── tests/
│   └── test_library.py        # Unit tests
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file




---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.8 or higher

### Setup

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd MyBooks
No external dependencies needed (uses Python standard library only)
Running the Application
Open terminal/command prompt
Navigate to the src/ folder:
bash


cd src
Run the application:
bash


python main.py
You'll see the menu. Choose an option (1-14) and follow prompts
💡 Usage Examples
Add a Book


Menu: Choose 1 (Add a new book)
Enter book ID: B001
Enter book title: Python for Beginners
Enter author name: John Doe
Enter ISBN: 978-1234567890
Enter genre: Programming
Enter quantity available: 5
✓ Book 'Python for Beginners' added successfully!
Register a Customer


Menu: Choose 4 (Register new customer)
Enter customer ID: C001
Enter customer name: Alice Smith
Enter email: alice@example.com
Enter phone number: 555-1234
✓ Customer 'Alice Smith' registered successfully!
Borrow a Book


Menu: Choose 6 (Borrow a book)
Enter book ID: B001
Enter customer ID: C001
✓ Book 'Python for Beginners' borrowed by Alice Smith. Due: 2026-09-25
View Overdue Books


Menu: Choose 10 (View overdue books)
--- OVERDUE BOOKS ---
⚠️  Python for Beginners (Customer: Alice Smith, Due: 2026-09-10)
🧪 Running Tests
From the tests/ folder:

bash


python test\_library.py
You should see:



🧪 Running tests...

✓ test\_add\_book passed
✓ test\_add\_customer passed
✓ test\_borrow\_book passed
✓ test\_return\_book passed
✓ test\_sell\_book passed
✓ test\_get\_overdue\_books passed
✓ test\_low\_stock\_books passed

✓ All tests passed!
📊 Data Storage
All data is automatically saved to CSV files in the data/ folder:

books.csv: Book inventory
customers.csv: Customer records
transactions.csv: Borrow/return/sell history
Data is loaded automatically on startup and saved when you exit.

🔧 Classes & Methods
Book
__init__(): Initialize a book
to_dict(): Convert to dictionary for storage
Customer
__init__(): Initialize a customer
to_dict(): Convert to dictionary for storage
Transaction
__init__(): Create borrow/return/sell transaction
mark_returned(): Record return date
to_dict(): Convert to dictionary for storage
LibraryManager
add_book(): Add new book to library
add_customer(): Register new customer
borrow_book(): Record borrowing
return_book(): Record return
sell_book(): Record sale
get_overdue_books(): List overdue items
get_customer_borrowed_books(): View customer's current borrowing
get_low_stock_books(): Items needing restock
get_sold_books_report(): Sales history
🐛 Error Handling
The app handles:

❌ Invalid book/customer IDs
❌ Insufficient stock
❌ Non-numeric inputs
❌ Duplicate registrations
❌ File I/O errors
All errors display user-friendly messages.

🎓 Learning Outcomes
This project demonstrates:

Object-Oriented Programming (OOP)
Data persistence with CSV
Exception handling
Input validation
CLI design
Unit testing
Code documentation
📝 License
Free to use and modify for educational purposes.

👨‍💻 Author
Created as a Python Intensive Capstone Project.

🤝 Future Enhancements
Add database (SQLite) instead of CSV
Implement email notifications for due dates
Add actual QR code scanning
Build a web interface (Flask/Django)
Add user authentication
PDF report generation



5. Press **Ctrl + S** to save

