import json

class Book:
    def __init__(self, title: str, author: str, isbn: str, publication_year: str, publisher: str, page_count: int, status: str = "Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.publisher = publisher
        self.page_count = page_count
        self.status = status

    def __str__(self):
        return f"""\n
                Title  :  {self.title}
                Author :  {self.author}
                ISBN   :  {self.isbn}
                Publication Year : {self.publication_year}
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
            "publication_year" : self.publication_year,
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
        publication_year = dict["publication_year"]
        publisher = dict["publisher"]
        page_count = dict["page_count"]
        status = dict["status"]
        return Book(title, author, isbn, publication_year, publisher, page_count, status)


class Library:

    def __init__(self, name: str, filename: str):
        self.name = name
        self._booklist = []
        self.filename = filename
    
    def add_book(self, book : Book):
        self._booklist.append(book)
        self.save_books()
    
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
        with open(self.filename, "r") as f:
            booklist_json = json.load(f)
        for i in booklist_json:
            self._booklist.append(Book.from_dict(i))

    def save_books(self):
        book_list_json = []
        for book in self._booklist:
            book_list_json.append(book.to_dict())
        
        with open(self.filename, "w") as f:
            json.dump(book_list_json, f)