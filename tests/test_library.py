"""
Unit tests for the Library Manager.
"""
import sys
sys.path.insert(0, '../src')

from library_manager import LibraryManager

def test_add_book():
    """Test adding a book."""
    library = LibraryManager()
    result = library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 5)
    assert 'added successfully' in result
    assert 'B001' in library.books
    print("✓ test_add_book passed")

def test_add_customer():
    """Test adding a customer."""
    library = LibraryManager()
    result = library.add_customer('C001', 'Alice', 'alice@email.com', '555-1234')
    assert 'registered successfully' in result
    assert 'C001' in library.customers
    print("✓ test_add_customer passed")

def test_borrow_book():
    """Test borrowing a book."""
    library = LibraryManager()
    library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 5)
    library.add_customer('C001', 'Alice', 'alice@email.com', '555-1234')
    
    result = library.borrow_book('B001', 'C001')
    assert 'borrowed' in result
    assert library.get_book('B001').quantity_available == 4
    print("✓ test_borrow_book passed")

def test_return_book():
    """Test returning a book."""
    library = LibraryManager()
    library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 5)
    library.add_customer('C001', 'Alice', 'alice@email.com', '555-1234')
    library.borrow_book('B001', 'C001')
    
    result = library.return_book('B001', 'C001')
    assert 'returned' in result
    assert library.get_book('B001').quantity_available == 5
    print("✓ test_return_book passed")

def test_sell_book():
    """Test selling a book."""
    library = LibraryManager()
    library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 5)
    
    result = library.sell_book('B001', 2)
    assert 'Sold' in result
    assert library.get_book('B001').quantity_available == 3
    assert library.get_book('B001').quantity_sold == 2
    print("✓ test_sell_book passed")

def test_get_overdue_books():
    """Test getting overdue books."""
    library = LibraryManager()
    library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 5)
    library.add_customer('C001', 'Alice', 'alice@email.com', '555-1234')
    library.borrow_book('B001', 'C001')
    
    # Manually set due date to past
    trans = list(library.transactions.values())[0]
    trans.due_date = '2020-01-01'
    
    overdue = library.get_overdue_books()
    assert len(overdue) > 0
    print("✓ test_get_overdue_books passed")

def test_low_stock_books():
    """Test getting low-stock books."""
    library = LibraryManager()
    library.add_book('B001', 'Python 101', 'John Doe', '12345', 'Programming', 2)
    
    low_stock = library.get_low_stock_books(threshold=3)
    assert len(low_stock) > 0
    print("✓ test_low_stock_books passed")

if __name__ == "__main__":
    print("\n🧪 Running tests...\n")
    test_add_book()
    test_add_customer()
    test_borrow_book()
    test_return_book()
    test_sell_book()
    test_get_overdue_books()
    test_low_stock_books()
    print("\n✓ All tests passed!\n")

