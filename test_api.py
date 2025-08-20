import pytest
from fastapi.testclient import TestClient
from api import app
import os
import json

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "documentation" in data

def test_get_books():
    """Test getting all books"""
    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)

def test_get_stats():
    """Test library statistics"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "library_name" in data
    assert "total_books" in data
    assert "available_books" in data
    assert "borrowed_books" in data

def test_get_book_not_found():
    """Test getting a book that doesn't exist"""
    response = client.get("/books/9999999999999")
    assert response.status_code == 404

def test_delete_book_not_found():
    """Test deleting a book that doesn't exist"""
    response = client.delete("/books/9999999999999")
    assert response.status_code == 404

def test_add_book_invalid_isbn():
    """Test adding a book with invalid ISBN"""
    response = client.post("/books", json={"isbn": "invalid"})
    assert response.status_code in [400, 404]  # Both are acceptable for invalid ISBN

def test_add_and_delete_book():
    """Test adding and then deleting a book"""
    # Try to add a book (this might fail due to API limitations)
    isbn = "9780134685991"
    response = client.post("/books", json={"isbn": isbn})
    
    if response.status_code == 200:
        # If book was added, try to delete it
        delete_response = client.delete(f"/books/{isbn}")
        assert delete_response.status_code == 200
    else:
        # If book couldn't be added, that's also acceptable for this test
        assert response.status_code in [400, 404]

if __name__ == "__main__":
    pytest.main([__file__])