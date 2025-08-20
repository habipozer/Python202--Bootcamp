# Library Management System

A comprehensive library management system built with Python, featuring both console interface and REST API functionality. This project allows users to manage books, search by ISBN, and integrate with external book databases.

## Features

- **Console Application**: Interactive command-line interface for library management
- **REST API**: FastAPI-based web service for programmatic access
- **ISBN Integration**: Automatic book data retrieval from Open Library API
- **Data Persistence**: JSON-based storage for book records
- **Comprehensive Testing**: Full test coverage for both console and API components

## Installation

### Clone the Repository
```bash
git clone https://github.com/habipozer/Python202--Bootcamp.git
cd Python202--Bootcamp
```

### Set Up Virtual Environment
```bash
python -m venv .venv
```

**Windows:**
```bash
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Console Application
Run the interactive terminal-based library management system:
```bash
python main.py
```

The console application provides the following features:
- Add books manually or by ISBN
- Remove books from library
- Search for books
- View all books in library
- Library statistics
- Load/save book data

### API Server
Start the FastAPI web server:
```bash
uvicorn api:app --reload
```

The API server will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Documentation

### Endpoints

#### `GET /`
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to Library Management API",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

#### `GET /books`
Retrieve all books in the library.

**Response:**
```json
[
  {
    "title": "Book Title",
    "author": "Author Name",
    "isbn": "9781234567890",
    "publish_date": "2023",
    "publisher": "Publisher Name",
    "page_count": 300,
    "status": "Available"
  }
]
```

#### `POST /books`
Add a new book to the library using ISBN.

**Request Body:**
```json
{
  "isbn": "9781234567890"
}
```

**Response:**
```json
{
  "title": "Retrieved Book Title",
  "author": "Author Name",
  "isbn": "9781234567890",
  "publish_date": "2023",
  "publisher": "Publisher Name",
  "page_count": 300,
  "status": "Available"
}
```

#### `GET /books/{isbn}`
Retrieve a specific book by ISBN.

**Response:**
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "9781234567890",
  "publish_date": "2023",
  "publisher": "Publisher Name",
  "page_count": 300,
  "status": "Available"
}
```

#### `DELETE /books/{isbn}`
Remove a book from the library by ISBN.

**Response:**
```json
{
  "message": "Book with ISBN 9781234567890 successfully deleted from the library",
  "success": true
}
```

#### `GET /stats`
Get library statistics.

**Response:**
```json
{
  "library_name": "Central Library",
  "total_books": 15,
  "available_books": 12,
  "borrowed_books": 3
}
```

#### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "Library Management API",
  "version": "1.0.0"
}
```

## Testing

Run the test suite to ensure all components work correctly:

### Console Application Tests
```bash
pytest test_library.py -v
```

### API Tests
```bash
pytest test_api.py -v
```

### Run All Tests
```bash
pytest -v
```

## Project Structure

```
├── main.py              # Console application entry point
├── library.py           # Core library and book classes
├── api.py              # FastAPI web service
├── test_library.py     # Console application tests
├── test_api.py         # API endpoint tests
├── library_data.json   # Book data storage
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **httpx**: HTTP client for external API requests
- **Pydantic**: Data validation and serialization
- **Pytest**: Testing framework

## Development

This project follows modern Python development practices:

- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception management
- **API Standards**: RESTful API design principles
- **Documentation**: Automatic API documentation generation
- **Testing**: High test coverage with pytest

## License

This project is part of a Python bootcamp curriculum and is intended for educational purposes.