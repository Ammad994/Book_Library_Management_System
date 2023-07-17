# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import messagebox

# Define the Book class to represent a book object
class Book:
    def __init__(self, title, author, genre, publication_date, is_read=False):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date
        self.is_read = is_read

# Define the Library class to manage a collection of books
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        # Add a book to the library
        self.books.append(book)

    def view_books(self):
        # Return the list of all books in the library
        return self.books

    def mark_as_read(self, book_index):
        # Mark a book as read based on its index in the list
        if 0 <= book_index < len(self.books):
            self.books[book_index].is_read = True
            return True
        return False

    def mark_as_unread(self, book_index):
        # Mark a book as unread based on its index in the list
        if 0 <= book_index < len(self.books):
            self.books[book_index].is_read = False
            return True
        return False

    def delete_book(self, book_index):
        # Delete a book from the library based on its index in the list
        if 0 <= book_index < len(self.books):
            del self.books[book_index]
            return True
        return False

    def search_books(self, keyword):
        # Search for books based on a keyword in the title or author
        found_books = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                found_books.append(book)
        return found_books

    def save_to_file(self, filename):
        # Save the library data to a JSON file
        data = []
        for book in self.books:
            data.append({
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "publication_date": book.publication_date,
                "is_read": book.is_read
            })
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def load_from_file(self, filename):
        # Load the library data from a JSON file
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for book_data in data:
                    book = Book(
                        title=book_data["title"],
                        author=book_data["author"],
                        genre=book_data["genre"],
                        publication_date=book_data["publication_date"],
                        is_read=book_data["is_read"]
                    )
                    self.books.append(book)
        except FileNotFoundError:
            pass

# Define the LibraryGUI class to create and manage the graphical user interface
class LibraryGUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Book Library Management System")

        # Create an instance of the Library class
        self.library = Library()
        self.library.load_from_file('library.json')

        # Create listbox to display books
        self.listbox = tk.Listbox(self.root, width=80)
        self.listbox.pack(padx=10, pady=10)

        # Create scrollbar for listbox
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Create labels and entry widgets for book details
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack()

        self.author_label = tk.Label(self.root, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.root, width=50)
        self.author_entry.pack()

        self.genre_label = tk.Label(self.root, text="Genre:")
        self.genre_label.pack()
        self.genre_entry = tk.Entry(self.root, width=50)
        self.genre_entry.pack()

        self.publication_label = tk.Label(self.root, text="Publication Date:")
        self.publication_label.pack()
        self.publication_entry = tk.Entry(self.root, width=50)
        self.publication_entry.pack()

        # Create buttons
        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.pack(pady=5)

        self.mark_read_button = tk.Button(self.root, text="Mark as Read", command=self.mark_as_read)
        self.mark_read_button.pack(pady=5)

        self.mark_unread_button = tk.Button(self.root, text="Mark as Unread", command=self.mark_as_unread)
        self.mark_unread_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Book", command=self.delete_book)
        self.delete_button.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Library", command=self.save_library)
        self.save_button.pack(pady=5)

        # Bind the listbox selection event to show details
        self.listbox.bind("<<ListboxSelect>>", self.show_details)

        # Initialize listbox with books
        self.refresh_listbox()

    def refresh_listbox(self):
        # Clear the listbox and add books from the library to it
        self.listbox.delete(0, tk.END)
        for book in self.library.view_books():
            status = "[Read]" if book.is_read else "[Unread]"
            self.listbox.insert(tk.END, f"{status} {book.title} by {book.author}")

    def show_details(self, event):
        # When a book is selected in the listbox, show its details in the entry widgets
        selected_index = self.listbox.curselection()
        if selected_index:
            book_index = selected_index[0]
            book = self.library.view_books()[book_index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(tk.END, book.title)
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(tk.END, book.author)
            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(tk.END, book.genre)
            self.publication_entry.delete(0, tk.END)
            self.publication_entry.insert(tk.END, book.publication_date)

    def add_book(self):
        # Get book details from entry widgets and add the book to the library
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        publication_date = self.publication_entry.get()
        if title and author and genre and publication_date:
            book = Book(title, author, genre, publication_date)
            self.library.add_book(book)
            self.refresh_listbox()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please fill all book details.")

    def mark_as_read(self):
        # Mark the selected book as read in the library
        selected_index = self.listbox.curselection()
        if selected_index:
            book_index = selected_index[0]
            if self.library.mark_as_read(book_index):
                self.refresh_listbox()
        else:
            messagebox.showerror("Error", "Please select a book to mark as read.")

    def mark_as_unread(self):
        # Mark the selected book as unread in the library
        selected_index = self.listbox.curselection()
        if selected_index:
            book_index = selected_index[0]
            if self.library.mark_as_unread(book_index):
                self.refresh_listbox()
        else:
            messagebox.showerror("Error", "Please select a book to mark as unread.")

    def delete_book(self):
        # Delete the selected book from the library
        selected_index = self.listbox.curselection()
        if selected_index:
            book_index = selected_index[0]
            if self.library.delete_book(book_index):
                self.refresh_listbox()
                self.clear_entries()
        else:
            messagebox.showerror("Error", "Please select a book to delete.")

    def search_books(self):
        # Search for books based on a keyword in the title or author
        keyword = self.title_entry.get()
        if keyword:
            found_books = self.library.search_books(keyword)
            if found_books:
                self.listbox.delete(0, tk.END)
                for book in found_books:
                    status = "[Read]" if book.is_read else "[Unread]"
                    self.listbox.insert(tk.END, f"{status} {book.title} by {book.author}")
            else:
                messagebox.showinfo("Search Results", "No matching books found.")
        else:
            self.refresh_listbox()

    def save_library(self):
        # Save the library data to a JSON file
        self.library.save_to_file('library.json')
        messagebox.showinfo("Save Library", "Library saved successfully.")

    def clear_entries(self):
        # Clear the entry widgets for book details
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.publication_entry.delete(0, tk.END)

def main():
    # Create the main Tkinter window and start the application
    root = tk.Tk()
    library_gui = LibraryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()