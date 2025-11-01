import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv
import os

class Book:
    def __init__(self, title, author, genre, total_copies=1):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies

    def display_details(self):
        status = f"{self.available_copies}/{self.total_copies} available"
        return [self.title, self.author, self.genre, status]

    @property
    def available(self):
        return self.available_copies > 0


class FictionBook(Book):
    def __init__(self, title, author, sub_genre, total_copies=1):
        super().__init__(title, author, f"Fiction ({sub_genre})", total_copies)


class NonFictionBook(Book):
    def __init__(self, title, author, subject, total_copies=1):
        super().__init__(title, author, f"Non-Fiction ({subject})", total_copies)


class ReferenceBook(Book):
    def __init__(self, title, author, field, total_copies=1):
        super().__init__(title, author, f"Reference ({field})", total_copies)

class MotivationalBook(Book):
    def __init__(self, title, author, theme, total_copies=1):
        super().__init__(title, author, f"Motivational ({theme})", total_copies)

class LibraryCatalog:
    def __init__(self):
        self.books = []
        self.history = []
        self.history_file = "library_history.csv"
        self.load_history()

    def add_book(self, book):
     
        for b in self.books:
            if b.title.lower() == book.title.lower() and b.author.lower() == book.author.lower():
                b.total_copies += book.total_copies
                b.available_copies += book.total_copies
                return
        self.books.append(book)

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def display_available_books(self):
        return [b for b in self.books if b.available]

    def add_history(self, book_title, action, user):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = [timestamp, book_title, action, user]
        self.history.append(entry)
        self.save_history()

    def save_history(self):
        with open(self.history_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Book Title", "Action", "User"])
            writer.writerows(self.history)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                self.history = [row for row in reader]

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Catalog System")
        self.root.geometry("1100x750")
        self.dark_mode = True

        self.catalog = LibraryCatalog()
        self.load_sample_books()

        self.style = ttk.Style()
        self.set_theme()

        title_frame = tk.Frame(root, bg=self.bg)
        title_frame.pack(fill="x", pady=8)
        tk.Label(
            title_frame,
            text="📚 Library Catalog System",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg,
            fg=self.highlight
        ).pack(pady=5)


        self.toolbar = tk.Frame(root, bg=self.bg)
        self.toolbar.pack(fill="x", pady=5)

        btn_style = {"side": "left", "padx": 6, "pady": 4}
        ttk.Button(self.toolbar, text="➕ Add", command=self.add_book_popup).pack(**btn_style)
        ttk.Button(self.toolbar, text="🔍 Search", command=self.search_popup).pack(**btn_style)
        ttk.Button(self.toolbar, text="📖 All", command=self.show_all_books).pack(**btn_style)
        ttk.Button(self.toolbar, text="✅ Available", command=self.show_available).pack(**btn_style)
        ttk.Button(self.toolbar, text="📥 Borrow", command=self.borrow_book).pack(**btn_style)
        ttk.Button(self.toolbar, text="📤 Return", command=self.return_book).pack(**btn_style)
        ttk.Button(self.toolbar, text="🌗 Theme", command=self.toggle_theme).pack(side="right", padx=8)

        frame_books = tk.LabelFrame(root, text="Library Catalog", bg=self.bg, fg=self.fg, padx=10, pady=10)
        frame_books.pack(fill="both", expand=True, padx=10, pady=8)

        columns = ("Title", "Author", "Genre", "Status")
        self.tree = ttk.Treeview(frame_books, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)
        self.tree.pack(fill="both", expand=True)

        frame_history = tk.LabelFrame(root, text="Borrow / Return History", bg=self.bg, fg=self.fg, padx=10, pady=10)
        frame_history.pack(fill="both", expand=True, padx=10, pady=8)

        history_cols = ("Timestamp", "Book Title", "Action", "User")
        self.tree_history = ttk.Treeview(frame_history, columns=history_cols, show="headings")
        for col in history_cols:
            self.tree_history.heading(col, text=col)
            self.tree_history.column(col, anchor="center", width=200)
        self.tree_history.pack(fill="both", expand=True)

        self.show_all_books()
        self.update_history_tree()

    def set_theme(self):
        if self.dark_mode:
            self.bg = "#1e1e1e"
            self.fg = "#ffffff"
            self.highlight = "#00BFFF"
        else:
            self.bg = "#f9f9f9"
            self.fg = "#000000"
            self.highlight = "#0078D7"

        self.root.configure(bg=self.bg)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"),
                             padding=5, background=self.highlight, foreground="white")
        self.style.map("TButton", background=[("active", "#005a9e")])
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10),
                             background=self.bg, fieldbackground=self.bg, foreground=self.fg)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.root.configure(bg=self.bg)

    def load_sample_books(self):
       samples = [
    FictionBook("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 25),
    FictionBook("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 16),
    FictionBook("To Kill a Mockingbird", "Harper Lee", "Drama", 35),
    FictionBook("Pride and Prejudice", "Jane Austen", "Romance", 16),
    FictionBook("The Hobbit", "J.R.R. Tolkien", "Adventure", 45),
    FictionBook("1984", "George Orwell", "Dystopian", 15),
    FictionBook("The Alchemist", "Paulo Coelho", "Philosophical", 10),
    MotivationalBook("The 7 Habits of Highly Effective People", "Stephen R. Covey", "Personal Development", 19),
    MotivationalBook("Think and Grow Rich", "Napoleon Hill", "Success", 18),
    MotivationalBook("You Can Win", "Shiv Khera", "Motivational", 16),
    MotivationalBook("The Power of Positive Thinking", "Norman Vincent Peale", "Inspiration", 18),
    MotivationalBook("Awaken the Giant Within", "Tony Robbins", "Self-Empowerment", 26),
    MotivationalBook("Start With Why", "Simon Sinek", "Leadership", 25),
    MotivationalBook("The Subtle Art of Not Giving a F*ck", "Mark Manson", "Mindset", 16),
    MotivationalBook("Can't Hurt Me", "David Goggins", "Resilience", 51),
    FictionBook("The Catcher in the Rye", "J.D. Salinger", "Classic", 25),
    NonFictionBook("Sapiens", "Yuval Noah Harari", "History", 26),
    NonFictionBook("Educated", "Tara Westover", "Memoir", 15),
    NonFictionBook("The Power of Habit", "Charles Duhigg", "Psychology", 15),
    NonFictionBook("Atomic Habits", "James Clear", "Self-Improvement", 21),
    NonFictionBook("Becoming", "Michelle Obama", "Biography", 25),
    ReferenceBook("Oxford English Dictionary", "Oxford Press", "Language", 55),
    ReferenceBook("Gray's Anatomy", "Henry Gray", "Medical", 16),
    ReferenceBook("The World Atlas", "National Geographic", "Geography", 35),
    FictionBook("Dance of Ice and Fire","George R.Martin ","FantasyStory On Dragons",23)
]

       for b in samples:
        self.catalog.add_book(b)

    def update_tree(self, books):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in books:
            self.tree.insert("", "end", values=b.display_details())

    def update_history_tree(self):
        for row in self.tree_history.get_children():
            self.tree_history.delete(row)
        for record in self.catalog.history:
            self.tree_history.insert("", "end", values=record)

    def show_all_books(self):
        self.update_tree(self.catalog.books)

    def show_available(self):
        self.update_tree(self.catalog.display_available_books())

    def borrow_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Book", "Please select a book to borrow.")
            return
        title = self.tree.item(selected[0])["values"][0]
        user_name = simpledialog.askstring("Borrow Book", "Enter your name:")
        if not user_name:
            return

        for b in self.catalog.books:
            if b.title == title:
                if b.available_copies > 0:
                    b.available_copies -= 1
                    self.catalog.add_history(title, "Borrowed", user_name)
                    self.show_all_books()
                    self.update_history_tree()
                    messagebox.showinfo("Success", f"{user_name} borrowed '{title}'.")
                else:
                    messagebox.showerror("Unavailable", "No copies left.")
                break

    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Book", "Please select a book to return.")
            return
        title = self.tree.item(selected[0])["values"][0]
        user_name = simpledialog.askstring("Return Book", "Enter your name:")
        if not user_name:
            return

        for b in self.catalog.books:
            if b.title == title:
                if b.available_copies < b.total_copies:
                    b.available_copies += 1
                    self.catalog.add_history(title, "Returned", user_name)
                    self.show_all_books()
                    self.update_history_tree()
                    messagebox.showinfo("Returned", f"{user_name} returned '{title}'.")
                else:
                    messagebox.showerror("Error", "All copies are already returned.")
                break

    def add_book_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Book")
        popup.geometry("400x350")
        popup.configure(bg=self.bg)

        tk.Label(popup, text="Title:", bg=self.bg, fg=self.fg).pack(pady=5)
        title_entry = tk.Entry(popup)
        title_entry.pack()

        tk.Label(popup, text="Author:", bg=self.bg, fg=self.fg).pack(pady=5)
        author_entry = tk.Entry(popup)
        author_entry.pack()

        tk.Label(popup, text="Type:", bg=self.bg, fg=self.fg).pack(pady=5)
        type_combo = ttk.Combobox(popup, values=["Fiction", "Non-Fiction", "Reference","Motivational"])
        type_combo.pack()

        tk.Label(popup, text="Extra Info:", bg=self.bg, fg=self.fg).pack(pady=5)
        extra_entry = tk.Entry(popup)
        extra_entry.pack()

        tk.Label(popup, text="Number of Copies:", bg=self.bg, fg=self.fg).pack(pady=5)
        copies_entry = tk.Entry(popup)
        copies_entry.insert(0, "1")
        copies_entry.pack()

        def confirm_add():
            title, author, btype, extra = title_entry.get(), author_entry.get(), type_combo.get(), extra_entry.get()
            try:
                copies = int(copies_entry.get())
            except ValueError:
                messagebox.showerror("Invalid", "Copies must be a number.")
                return

            if not title or not author or not btype:
                messagebox.showwarning("Warning", "Please fill all fields.")
                return

            if btype == "Fiction":
                book = FictionBook(title, author, extra or "General", copies)
            elif btype == "Non-Fiction":
                book = NonFictionBook(title, author, extra or "General", copies)
            else:
                book = ReferenceBook(title, author, extra or "General", copies)

            self.catalog.add_book(book)
            self.show_all_books()
            popup.destroy()
            messagebox.showinfo("Added", f"'{title}' added ({copies} copies).")

        ttk.Button(popup, text="Add Book", command=confirm_add).pack(pady=10)

    def search_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Search Book")
        popup.geometry("400x200")
        popup.configure(bg=self.bg)

        tk.Label(popup, text="Search by Title or Author:", bg=self.bg, fg=self.fg).pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack()

        def do_search():
            q = entry.get().strip()
            if not q:
                return
            books = self.catalog.search_by_title(q) + self.catalog.search_by_author(q)
            if books:
                self.update_tree(books)
            else:
                messagebox.showinfo("Not Found", "No matching books found.")
            popup.destroy()

        ttk.Button(popup, text="Search", command=do_search).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
