import pytest
import os
import json
from library import Book, Library


def test_str_formatting():

    book = Book("Test", "Author", "0-345-24223-8", "2020", "Pub", 100)
    
    result = str(book)
    
    assert "Title  :" in result
    assert "Author :" in result
    assert "ISBN   :" in result
    assert "Publication Year :" in result
    assert "Publisher        :" in result
    assert "Page Count       :" in result
    assert "Status           :" in result

def test_borrow_book():
    book = Book("Test", "Author", "0-345-24223-8", "2020", "Pub", 100)
    book.borrow()
    assert book.status == "Borrowed"

def test_return_book():
    
    book = Book("Test", "Author", "0-345-24223-8", "2020", "Pub", 100)
    book.borrow()
    
    book.return_book()
    
    assert book.status == "Available"

def test_book_to_dict():

    book = Book("Test", "Author", "0-345-24223-8", "2020", "Pub", 100)

    expected_dict = {"title": "Test",
                    "author": "Author",  
                    "isbn": "0-345-24223-8",
                    "publication_year": "2020",
                    "publisher": "Pub",  
                    "page_count": 100,
                    "status": "Available"}

    assert expected_dict == book.to_dict()

def test_from_dict():
    test_dict = {"title": "Test",
                "author": "Author",  
                "isbn": "0-345-24223-8",
                "publication_year": "2020",
                "publisher": "Pub",  
                "page_count": 100,
                "status": "Available"}

    book = Book.from_dict(test_dict)

    assert book.title == "Test"
    assert book.author == "Author"
    assert book.isbn == "0-345-24223-8"
    assert book.publication_year == "2020"
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


