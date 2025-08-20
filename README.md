# Library Management System

A simple library management system built with Python. Includes both console interface and REST API.

## Features

- Console application for library management
- REST API with FastAPI
- ISBN lookup from Open Library
- JSON data storage
- Unit tests

## Setup

Clone the repository:
```bash
git clone https://github.com/habipozer/Python202--Bootcamp.git
cd Python202--Bootcamp
```

Create virtual environment and install dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Usage

### Console App
```bash
python main.py
```

### API Server
```bash
uvicorn api:app --reload
```

API will be available at http://localhost:8000
Docs at http://localhost:8000/docs

## API Endpoints

- `GET /books` - List all books
  ```json
  // Response: Array of book objects
  [
    {
      "title": "Book Title",
      "author": "Author Name", 
      "isbn": "9781234567890",
      "publish_date": "2023",
      "publisher": "Publisher",
      "page_count": 300,
      "status": "Available"
    }
  ]
  ```

- `POST /books` - Add book by ISBN
  ```json
  // Request body:
  {"isbn": "9781234567890"}
  
  // Response: Book object
  {
    "title": "Retrieved Book Title",
    "author": "Author Name",
    "isbn": "9781234567890", 
    "publish_date": "2023",
    "publisher": "Publisher",
    "page_count": 300,
    "status": "Available"
  }
  ```

- `DELETE /books/{isbn}` - Remove book
  ```json
  // Response:
  {
    "message": "Book with ISBN {isbn} successfully deleted",
    "success": true
  }
  ```

- `GET /books/{isbn}` - Get specific book
  ```json
  // Response: Book object (same format as POST /books)
  ```

- `GET /stats` - Library statistics
  ```json
  // Response:
  {
    "library_name": "Central Library",
    "total_books": 15,
    "available_books": 12, 
    "borrowed_books": 3
  }
  ```

## Testing

```bash
pytest test_library.py -v    # Console tests
pytest test_api.py -v        # API tests
```

## Project Structure

```
├── main.py              # Console app
├── library.py           # Core classes
├── api.py              # FastAPI server
├── test_library.py     # Tests
├── test_api.py         # API tests
├── library_data.json   # Data storage
└── requirements.txt    # Dependencies
```

## Dependencies

- FastAPI - Web framework
- httpx - HTTP client
- Pydantic - Data validation
- Pytest - Testing
