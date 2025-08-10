class Book:
    def __init__(self, title: str, author: str, isbn: str, publication_year: str, publisher: str, page_count: int, is_borrowed: bool = False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.publisher = publisher
        self.page_count = page_count
        self.is_borrowed = is_borrowed

    def __str__(self):
        return f"""\n
                Title  :  {self.title}
                Author :  {self.author}
                ISBN   :  {self.isbn}
                Publication Year : {self.publication_year}
                Publisher        : {self.publisher}
                Page Count       : {self.page_count}
                Status           : {"Already Borrowed" if self.is_borrowed else "Available"}
                    """


class Library:

    def __init__(self, name: str):
        self.name = name
        self._booklist = []