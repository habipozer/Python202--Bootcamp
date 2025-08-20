import pytest
import os
import json
import httpx
from unittest.mock import patch, Mock
from library import Book, Library


def test_str_formatting():

    book = Book("Test", "Author", "6054584294", "2020", "Pub", 100)
    
    result = str(book)
    
    assert "Title  :" in result
    assert "Author :" in result
    assert "ISBN   :" in result
    assert "Publish Date :" in result
    assert "Publisher        :" in result
    assert "Page Count       :" in result
    assert "Status           :" in result

def test_borrow_book():
    book = Book("Test", "Author", "6054584294", "2020", "Pub", 100)
    book.borrow()
    assert book.status == "Borrowed"

def test_return_book():
    
    book = Book("Test", "Author", "6054584294", "2020", "Pub", 100)
    book.borrow()
    
    book.return_book()
    
    assert book.status == "Available"

def test_book_to_dict():

    book = Book("Test", "Author", "6054584294", "2020", "Pub", 100)

    expected_dict = {"title": "Test",
                    "author": "Author",  
                    "isbn": "6054584294",
                    "publish_date": "2020",
                    "publisher": "Pub",  
                    "page_count": 100,
                    "status": "Available"}

    assert expected_dict == book.to_dict()

def test_from_dict():
    test_dict = {"title": "Test",
                "author": "Author",  
                "isbn": "6054584294",
                "publish_date": "2020",
                "publisher": "Pub",  
                "page_count": 100,
                "status": "Available"}

    book = Book.from_dict(test_dict)

    assert book.title == "Test"
    assert book.author == "Author"
    assert book.isbn == "6054584294"
    assert book.publish_date == "2020"
    assert book.publisher == "Pub"
    assert book.page_count == 100
    assert book.status == "Available"


# ========== LIBRARY TESTS ==========

def test_library_creation():
    library = Library("Test Library", "test.json")
    
    assert library.name == "Test Library"
    assert library.filename == "test.json"
    assert library._booklist == []

def test_add_book():

    library = Library("Test Library", "test_add.json")
    book = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    
    library.add_book(book)
    
    assert len(library._booklist) == 1
    assert library._booklist[0] == book
    
    if os.path.exists("test_add.json"):
        os.remove("test_add.json")

def test_add_multiple_books():
    library = Library("Test Library", "test_multiple.json")
    book1 = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    book2 = Book("Dune", "Frank Herbert", "978-0441013593", "1965", "Ace", 688)
    
    library.add_book(book1)
    library.add_book(book2)
    
    assert len(library._booklist) == 2
    assert book1 in library._booklist
    assert book2 in library._booklist
    
    if os.path.exists("test_multiple.json"):
        os.remove("test_multiple.json")

def test_remove_book_success():
    library = Library("Test Library", "test_remove.json")
    book = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    library.add_book(book)
    
    result = library.remove_book("978-0451524935")
    
    assert result == True
    assert len(library._booklist) == 0
    
    if os.path.exists("test_remove.json"):
        os.remove("test_remove.json")

def test_remove_book_not_found():
    library = Library("Test Library", "test_remove_fail.json")
    
    result = library.remove_book("999-9999999999")
    
    assert result == False
    assert len(library._booklist) == 0
    
    if os.path.exists("test_remove_fail.json"):
        os.remove("test_remove_fail.json")

def test_find_book_success():
    library = Library("Test Library", "test_find.json")
    book = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    library.add_book(book)
    
    result = library.find_book("978-0451524935")
    
    assert result == True
    
    if os.path.exists("test_find.json"):
        os.remove("test_find.json")

def test_find_book_not_found():
    library = Library("Test Library", "test_find_fail.json")
    
    result = library.find_book("999-9999999999")
    
    assert result == False

    if os.path.exists("test_find_fail.json"):
        os.remove("test_find_fail.json")

def test_save_and_load_books():
    library = Library("Test Library", "test_save_load.json")
    book1 = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    book2 = Book("Dune", "Frank Herbert", "978-0441013593", "1965", "Ace", 688)
    
    library.add_book(book1)
    library.add_book(book2)

    new_library = Library("New Library", "test_save_load.json")
    new_library.load_books()
    

    assert len(new_library._booklist) == 2
    assert new_library._booklist[0].title == "1984"
    assert new_library._booklist[1].title == "Dune"
    

    if os.path.exists("test_save_load.json"):
        os.remove("test_save_load.json")

def test_load_books_file_not_found():
    library = Library("Test Library", "nonexistent.json")
    
    with pytest.raises(FileNotFoundError):
        library.load_books()

def test_list_books_empty():
    library = Library("Test Library", "test_empty.json")
    
    library.list_books() 
    assert len(library._booklist) == 0

def test_list_books_with_content(capsys):
    library = Library("Test Library", "test_list.json")
    book = Book("1984", "George Orwell", "978-0451524935", "1949", "Signet", 328)
    library.add_book(book)

    library.list_books()

    captured = capsys.readouterr()
    assert "1984" in captured.out
    assert "George Orwell" in captured.out
    
    if os.path.exists("test_list.json"):
        os.remove("test_list.json")


def test_add_book_isbn_success():
    """Test successful ISBN book addition via API"""
    library = Library("Test Library", "test_isbn.json")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "title": "Test Book",
        "authors": [{"key": "/authors/OL123A"}],
        "publish_date": "2020",
        "publishers": ["Test Publisher"],
        "number_of_pages": 200
    }
    
    mock_author_response = Mock()
    mock_author_response.json.return_value = {
        "name": "Test Author"
    }
    
    with patch('httpx.get', side_effect=[mock_response, mock_author_response]):
        library.add_book_isbn("9780123456789")
    
    assert len(library._booklist) == 1
    assert library._booklist[0].title == "Test Book"
    assert library._booklist[0].author == "Test Author"
    assert library._booklist[0].isbn == "9780123456789"
    
    if os.path.exists("test_isbn.json"):
        os.remove("test_isbn.json")


def test_add_book_isbn_404_error():
    """Test ISBN not found (404 error)"""
    library = Library("Test Library", "test_isbn_404.json")
    
    # Mock 404 response
    mock_response = Mock()
    mock_response.status_code = 404
    
    with patch('httpx.get') as mock_get:
        mock_get.return_value = mock_response
        mock_get.side_effect = httpx.HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        
        library.add_book_isbn("9999999999999")
    
    # Should not add any book
    assert len(library._booklist) == 0
    
    if os.path.exists("test_isbn_404.json"):
        os.remove("test_isbn_404.json")


def test_add_book_isbn_302_redirect():
    """Test handling of 302 redirect error"""
    library = Library("Test Library", "test_isbn_302.json")
    
    # Mock 302 response for primary request
    mock_302_response = Mock()
    mock_302_response.status_code = 302
    
    # Mock successful alternative API response
    mock_alt_response = Mock()
    mock_alt_response.status_code = 200
    mock_alt_response.json.return_value = {
        "ISBN:9780123456789": {
            "title": "Redirect Test Book",
            "authors": [{"name": "Redirect Author"}],
            "publish_date": "2021",
            "publishers": [{"name": "Redirect Publisher"}],
            "number_of_pages": 150
        }
    }
    
    with patch('httpx.get') as mock_get:
        # First call raises 302, second call succeeds
        mock_get.side_effect = [
            httpx.HTTPStatusError("Found", request=Mock(), response=mock_302_response),
            mock_alt_response
        ]
        
        library.add_book_isbn("9780123456789")
    
    assert len(library._booklist) == 1
    assert library._booklist[0].title == "Redirect Test Book"
    assert library._booklist[0].author == "Redirect Author"
    
    if os.path.exists("test_isbn_302.json"):
        os.remove("test_isbn_302.json")


def test_add_book_isbn_connection_error():
    """Test network connection error handling"""
    library = Library("Test Library", "test_isbn_connection.json")
    
    with patch('httpx.get') as mock_get:
        mock_get.side_effect = httpx.ConnectError("Connection failed")
        
        library.add_book_isbn("9780123456789")
    
    # Should not add any book
    assert len(library._booklist) == 0
    
    if os.path.exists("test_isbn_connection.json"):
        os.remove("test_isbn_connection.json")


def test_add_book_isbn_no_authors():
    """Test API response with no authors"""
    library = Library("Test Library", "test_isbn_no_authors.json")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "title": "No Author Book",
        "authors": [],  # No authors
        "publish_date": "2020",
        "publishers": ["Test Publisher"],
        "number_of_pages": 100
    }
    
    with patch('httpx.get', return_value=mock_response):
        library.add_book_isbn("9780123456789")
    
    assert len(library._booklist) == 1
    assert library._booklist[0].author == "Unknown Author"
    
    if os.path.exists("test_isbn_no_authors.json"):
        os.remove("test_isbn_no_authors.json")


def test_add_book_isbn_minimal_data():
    """Test API response with minimal data"""
    library = Library("Test Library", "test_isbn_minimal.json")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "title": "Minimal Book"
        # Missing: authors, publish_date, publishers, number_of_pages
    }
    
    with patch('httpx.get', return_value=mock_response):
        library.add_book_isbn("9780123456789")
    
    assert len(library._booklist) == 1
    book = library._booklist[0]
    assert book.title == "Minimal Book"
    assert book.author == "Unknown Author"
    assert book.publish_date == "Unknown"
    assert book.publisher == "Unknown Publisher"
    assert book.page_count == 0
    
    if os.path.exists("test_isbn_minimal.json"):
        os.remove("test_isbn_minimal.json")


