from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from library import Library, Book
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="Library Management API",
    description="A simple library management system with FastAPI",
    version="1.0.0"
)

# Initialize library instance
library = Library("Central Library", "library_data.json")

# Load existing books on startup
try:
    library.load_books()
except FileNotFoundError:
    print("No existing library data found. Starting with empty library.")
except Exception as e:
    print(f"Error loading library data: {e}")

# Pydantic models for request/response
class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str
    publish_date: str
    publisher: str
    page_count: int
    status: str

class ISBNRequest(BaseModel):
    isbn: str

class MessageResponse(BaseModel):
    message: str
    success: bool

# Convert Book object to BookResponse
def book_to_response(book: Book) -> BookResponse:
    return BookResponse(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        publish_date=book.publish_date,
        publisher=book.publisher,
        page_count=book.page_count,
        status=book.status
    )

# API Endpoints

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Library Management API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "GET /books": "Get all books",
            "POST /books": "Add book by ISBN",
            "DELETE /books/{isbn}": "Delete book by ISBN"
        }
    }

@app.get("/books", response_model=List[BookResponse])
async def get_all_books():
    """Get all books in the library"""
    try:
        books = [book_to_response(book) for book in library._booklist]
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving books: {str(e)}")

@app.post("/books", response_model=BookResponse)
async def add_book_by_isbn(isbn_request: ISBNRequest):
    """Add a book to the library using ISBN"""
    try:
        # Check if book already exists
        for book in library._booklist:
            if book.isbn == isbn_request.isbn:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Book with ISBN {isbn_request.isbn} already exists in the library"
                )
        
        # Store original length to check if book was added
        original_length = len(library._booklist)
        
        # Add book using the library method
        library.add_book_isbn(isbn_request.isbn)
        
        # Check if book was actually added
        if len(library._booklist) <= original_length:
            raise HTTPException(
                status_code=404, 
                detail=f"Book with ISBN {isbn_request.isbn} not found in Open Library database"
            )
        
        # Return the newly added book
        new_book = library._booklist[-1]
        return book_to_response(new_book)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding book: {str(e)}")

@app.delete("/books/{isbn}", response_model=MessageResponse)
async def delete_book(isbn: str):
    """Delete a book from the library by ISBN"""
    try:
        # Check if book exists before deletion
        book_found = False
        for book in library._booklist:
            if book.isbn == isbn:
                book_found = True
                break
        
        if not book_found:
            raise HTTPException(
                status_code=404, 
                detail=f"Book with ISBN {isbn} not found in the library"
            )
        
        # Remove the book
        success = library.remove_book(isbn)
        
        if success:
            return MessageResponse(
                message=f"Book with ISBN {isbn} successfully deleted from the library",
                success=True
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to delete book with ISBN {isbn}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting book: {str(e)}")

@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str):
    """Get a specific book by ISBN"""
    try:
        for book in library._booklist:
            if book.isbn == isbn:
                return book_to_response(book)
        
        raise HTTPException(
            status_code=404, 
            detail=f"Book with ISBN {isbn} not found in the library"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving book: {str(e)}")

@app.get("/stats", response_model=dict)
async def get_library_stats():
    """Get library statistics"""
    try:
        total_books = len(library._booklist)
        borrowed_books = sum(1 for book in library._booklist if book.status == "Borrowed")
        available_books = total_books - borrowed_books
        
        return {
            "library_name": library.name,
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving statistics: {str(e)}")

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Library Management API",
        "version": "1.0.0"
    }