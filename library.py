import json
import httpx

class Book:
    def __init__(self, title: str, author: str, isbn: str, publish_date: str, publisher: str, page_count: int, status: str = "Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publish_date = publish_date
        self.publisher = publisher
        self.page_count = page_count
        self.status = status

    def __str__(self):
        return f"""\n
                Title  :  {self.title}
                Author :  {self.author}
                ISBN   :  {self.isbn}
                Publish Date : {self.publish_date}
                Publisher        : {self.publisher}
                Page Count       : {self.page_count}
                Status           : {"Already Borrowed" if self.status == "Borrowed" else "Available"}
                    """
    def borrow(self):
        self.status = "Borrowed"
    def return_book(self):
        self.status = "Available"
    
    def to_dict(self):
        dict = {
            "title" : self.title,
            "author" : self.author,
            "isbn" : self.isbn,
            "publish_date" : self.publish_date,
            "publisher" : self.publisher,
            "page_count" : self.page_count,
            "status" : self.status
        }
        return dict
    
    @staticmethod
    def from_dict(dict : dict):
        title = dict["title"]
        author = dict["author"]
        isbn = dict["isbn"]
        publish_date = dict["publish_date"]
        publisher = dict["publisher"]
        page_count = dict["page_count"]
        status = dict["status"]
        return Book(title, author, isbn, publish_date, publisher, page_count, status)


class Library:

    def __init__(self, name: str, filename: str):
        self.name = name
        self._booklist = []
        self.filename = filename
    
    def add_book(self, book : Book):
        self._booklist.append(book)
        self.save_books()
    
    def add_book_isbn(self, isbn : str):
        
        OPEN_LIBRARY_URL = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            # Add timeout and explicit redirect following
            response = httpx.get(OPEN_LIBRARY_URL, timeout=10.0, follow_redirects=True)
            response.raise_for_status()
            data = response.json()
            title = data.get("title","Unknown Title")
            authors = data.get("authors", [])

            if authors:
                author_key = authors[0].get("key", "")
                
                author_response = httpx.get(f"https://openlibrary.org{author_key}.json", timeout=10.0, follow_redirects=True)
                author_data = author_response.json()
                author = author_data.get("name", "Unknown Author")
            else:
                author = "Unknown Author"
            
            publish_date = data.get("publish_date","Unknown")
            publishers = data.get("publishers", [])
            publisher = publishers[0] if publishers else "Unknown Publisher"
            page_count = data.get("number_of_pages", 0)
            
            book = Book(title, author, isbn, publish_date, publisher, page_count)    
            self._booklist.append(book)
            self.save_books()
            print(f"Book successfully added: {title}")
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 302:
                print(f"Redirect error for ISBN {isbn}. Trying alternative method...")
                # Try alternative URL format
                try:
                    alt_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
                    alt_response = httpx.get(alt_url, timeout=10.0)
                    alt_response.raise_for_status()
                    alt_data = alt_response.json()
                    
                    if f"ISBN:{isbn}" in alt_data:
                        book_data = alt_data[f"ISBN:{isbn}"]
                        title = book_data.get("title", "Unknown Title")
                        authors = book_data.get("authors", [])
                        author = authors[0].get("name", "Unknown Author") if authors else "Unknown Author"
                        publish_date = book_data.get("publish_date", "Unknown")
                        publishers = book_data.get("publishers", [])
                        publisher = publishers[0].get("name", "Unknown Publisher") if publishers else "Unknown Publisher"
                        page_count = book_data.get("number_of_pages", 0)
                        
                        book = Book(title, author, isbn, publish_date, publisher, page_count)
                        self._booklist.append(book)
                        self.save_books()
                        print(f"Book successfully added via alternative method: {title}")
                    else:
                        print(f"Book with ISBN {isbn} not found via alternative method")
                except Exception as alt_e:
                    print(f"Alternative method also failed: {alt_e}")
            elif e.response.status_code == 404:
                print(f"Error: Book with ISBN {isbn} not found!")
            else:
                print(f"HTTP Error: {e.response.status_code}")
        except httpx.RequestError as e:
            print(f"Connection error: {e}")
        except httpx.ConnectError as e:
            print("Network connection error")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def remove_book(self, isbn : str):
        for i, book in enumerate(self._booklist):
            if book.isbn == isbn: 
                del self._booklist[i]
                self.save_books()
                return True
        return False
    
    def list_books(self):
        for book in self._booklist:
            print(book)
    
    def find_book(self, isbn : str):
        for i, book in enumerate(self._booklist):
            if book.isbn == isbn : 
                print(book)
                return True
        print("The book was not found in this library")
        return False
    
    def load_books(self):
        self._booklist.clear()
        try:
            with open(self.filename, "r") as f:
                booklist_json = json.load(f)
            for i in booklist_json:
                try:
                    book = Book.from_dict(i)
                    self._booklist.append(book)
                except Exception as e:
                    print(f"Error loading book from JSON: {e}")
                    print(f"Skipping invalid book data: {i}")
        except FileNotFoundError:
           print("library_data.json could not be found.")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
        except Exception as e:
            print(f"Unexpected error loading books: {e}")

    def save_books(self):
        book_list_json = []
        for book in self._booklist:
            book_list_json.append(book.to_dict())
        
        with open(self.filename, "w") as f:
            json.dump(book_list_json, f)