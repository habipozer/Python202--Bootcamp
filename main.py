from library import Library, Book


def print_menu():
    print("\n" + "="*60)
    print("LIBRARY MANAGEMENT SYSTEM".center(60))
    print("="*60)
    print("┌─ Main Menu ────────────────────────────────────────────┐")
    print("│                                                        │")
    print("│  1. Add Book                                           │")
    print("│  2. Remove Book (by ISBN)                             │")
    print("│  3. Search Book (by ISBN)                             │")
    print("│  4. List All Books                                    │")
    print("│  5. Load Books (from file)                            │")
    print("│  6. Library Statistics                                │")
    print("│  0. Exit                                              │")
    print("│                                                        │")
    print("└────────────────────────────────────────────────────────┘")
    print()

def get_book_input():
    """Get book information from user"""
    print("\nNew Book Information:")
    print("-" * 30)
    title = input("Book Title: ")
    author = input("Author: ")
    isbn = input("ISBN: ")
    publication_year = input("Publication Year: ")
    publisher = input("Publisher: ")
    
    while True:
        try:
            page_count = int(input("Page Count: "))
            break
        except ValueError:
            print("Please enter a valid number!")
    
    return Book(title, author, isbn, publication_year, publisher, page_count)

def show_statistics(library):
    """Display library statistics"""
    total_books = len(library._booklist)
    borrowed_books = sum(1 for book in library._booklist if book.status == "Borrowed")
    available_books = total_books - borrowed_books
    
    print(f"\n{library.name} Library Statistics:")
    print("─" * 45)
    print(f"Total Books        : {total_books}")
    print(f"Available Books    : {available_books}")
    print(f"Borrowed Books     : {borrowed_books}")
    print("─" * 45)

def main():
    library = Library("Yigit Okur Library", "library_data.json")

    try:
        library.load_books()
        print("Books were successfully loaded into the library")
    except FileNotFoundError:
        print("JSON file was not found. New library created.")
    except Exception as e:
        print(f"A problem occurred during the loading process, error: {e}")

    while True:
        print_menu()
        choice = input("Please enter your choice (0-6): ").strip()

        match choice:
            case "1":
                print("\n>> Add Book Operation")
                try:
                    new_book = get_book_input()
                    library.add_book(new_book)
                    print(f"'{new_book.title}' was successfully added!")
                except Exception as e:
                    print(f"Error: {e}")
            
            case "2":
                print("\n>> Remove Book Operation")
                isbn = input("Enter the ISBN of the book to remove: ")
                if library.remove_book(isbn):
                    print("Book was successfully removed!")
                else:
                    print("Book was not found!")
            
            case "3":
                print("\n>> Search Book Operation")
                isbn = input("Enter the ISBN of the book to search: ")
                if not library.find_book(isbn):
                    print("Would you like to search for another book?")
            
            case "4":
                print(f"\n>> {library.name} - All Books")
                if library._booklist:
                    library.list_books()
                else:
                    print("No books are currently available in the library.")
            
            case "5":
                print("\n>> Load Books Operation")
                try:
                    library.load_books()
                    print("Books were successfully loaded!")
                except FileNotFoundError:
                    print("File was not found!")
                except Exception as e:
                    print(f"Error: {e}")
            
            case "6":
                show_statistics(library)
            
            case "0":
                print("\n" + "="*50)
                print("Exiting the library system...".center(50))
                print("Thank you!".center(50))
                print("="*50)
                break
            
            case _:
                print("Invalid choice! Please enter a value between 0-6.")
        
        # Wait to continue
        if choice != "0":
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

