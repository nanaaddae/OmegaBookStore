import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def connect():
    conn = sqlite3.connect("Books.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE if not exists Books(Title TEXT, Year INTEGER, Author TEXT, ISBN TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

def insert(title, year, author, ISBN):
    connect()
    conn = sqlite3.connect("Books.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO BOOKS VALUES (?,?,?,?)", (title, year, author, ISBN))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
    except sqlite3.IntegrityError:
        print("ISBN already exists!")
    finally:
        conn.close()

def edit_book():
    # Get ISBN from user input
    isbn_to_edit = simpledialog.askstring("Edit Book", "Enter ISBN to edit:")

    if isbn_to_edit:
        # Connect to the database
        connect()
        conn = sqlite3.connect("Books.db")
        cur = conn.cursor()

        # Retrieve the book details based on ISBN
        cur.execute("SELECT * FROM BOOKS WHERE ISBN=?", (isbn_to_edit,))
        book_details = cur.fetchone()

        conn.close()

        if book_details:
            # Open a pop-up window for editing
            edit_window = tk.Toplevel(root)
            edit_window.title("Edit Book")
            edit_window.geometry("300x200")

            # Create labels and entry widgets for editing
            label_title = tk.Label(edit_window, text="Title:")
            label_title.grid(row=0, column=0, padx=10, pady=5)
            entry_title = tk.Entry(edit_window)
            entry_title.grid(row=0, column=1, padx=10, pady=5)
            entry_title.insert(tk.END, book_details[0])

            label_author = tk.Label(edit_window, text="Author:")
            label_author.grid(row=1, column=0, padx=10, pady=5)
            entry_author = tk.Entry(edit_window)
            entry_author.grid(row=1, column=1, padx=10, pady=5)
            entry_author.insert(tk.END, book_details[2])

            label_year = tk.Label(edit_window, text="Year:")
            label_year.grid(row=2, column=0, padx=10, pady=5)
            entry_year = tk.Entry(edit_window)
            entry_year.grid(row=2, column=1, padx=10, pady=5)
            entry_year.insert(tk.END, book_details[1])

            label_isbn = tk.Label(edit_window, text="ISBN:")
            label_isbn.grid(row=3, column=0, padx=10, pady=5)
            entry_isbn = tk.Entry(edit_window)
            entry_isbn.grid(row=3, column=1, padx=10, pady=5)
            entry_isbn.insert(tk.END, book_details[3])

            def save_changes():
                # Get values from entry widgets
                new_title = entry_title.get()
                new_author = entry_author.get()
                new_year = entry_year.get()
                new_isbn = entry_isbn.get()

                # Update the database with new values
                conn = sqlite3.connect("Books.db")
                cur = conn.cursor()
                cur.execute("UPDATE BOOKS SET Title=?, Author=?, Year=?, ISBN=? WHERE ISBN=?", (new_title, new_author, new_year, new_isbn, isbn_to_edit))
                conn.commit()
                conn.close()

                # Close the pop-up window
                edit_window.destroy()

                # Refresh the displayed books after editing
                see_all_books()

            # Create a button to save changes
            save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
            save_button.grid(row=4, column=0, columnspan=2, pady=10)


def see_all_books(title_filter="", author_filter="", year_filter="", sort_key="", sort_order=""):
    connect()
    conn = sqlite3.connect("Books.db")
    cur = conn.cursor()

    # Build SQL query based on filters and sorting options
    query = "SELECT * FROM BOOKS WHERE 1"
    if title_filter:
        query += f" AND Title LIKE '%{title_filter}%'"
    if author_filter:
        query += f" AND Author LIKE '%{author_filter}%'"
    if year_filter:
        query += f" AND Year = {year_filter}"
    if sort_key:
        query += f" ORDER BY {sort_key} {sort_order}"

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    # Clear existing text in the Text widget
    text_box.config(state=tk.NORMAL)
    text_box.delete(1.0, tk.END)

    # Insert new text into the Text widget in a tabular format
    text_box.insert(tk.END, "Title\t\tYear\tAuthor\t\tISBN\n")
    text_box.insert(tk.END, "="*50 + "\n")  # Separator line

    for row in rows:
        if all(value is not None for value in row):
            text_box.insert(tk.END, f"{row[0]}\t\t{row[1]}\t{row[2]}\t\t{row[3]}\n")

    text_box.config(state=tk.DISABLED)


def delete_book():
    isbn_to_delete = simpledialog.askstring("Delete Book", "Enter ISBN to delete:")

    if isbn_to_delete:
        confirmation = messagebox.askokcancel("Confirmation",
                                              f"Are you sure you want to delete the book with ISBN: {isbn_to_delete}?")
        if confirmation:
            connect()
            conn = sqlite3.connect("Books.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM BOOKS WHERE ISBN=?", (isbn_to_delete,))
            conn.commit()
            conn.close()
            see_all_books()  # Refresh the displayed books after deletion


def quit_application():
    confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to quit?")
    if confirmation:
        root.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.title("Omega Bookstore")
root.configure(bg='Yellow')

# Create labels for the application
label_title = tk.Label(root, text="Title", bg='green')
label_title.place(x=0, y=0)

label_author = tk.Label(root, text="Author", bg='green')
label_author.place(x=0, y=100)

label_year = tk.Label(root, text="Year", bg='green')
label_year.place(x=150, y=0)

label_isbn = tk.Label(root, text="ISBN", bg='green')
label_isbn.place(x=150, y=100)

Omega = tk.Label(root, text="Omega Bookstore", bg='green', font=("Arial", 30))
Omega.place(x=474, y=0)

root.geometry("1024x576")

# Create StringVar variables for the Entry widgets
e1_var = tk.StringVar(value="")
e2_var = tk.StringVar(value="")
e3_var = tk.StringVar(value="")
e4_var = tk.StringVar(value="")

# Create text fields for the application and place them in the appropriate positions
e1 = tk.Entry(root, textvariable=e1_var)
e1.place(x=0, y=40)

e2 = tk.Entry(root, textvariable=e2_var)
e2.place(x=0, y=140)

e3 = tk.Entry(root, textvariable=e3_var)
e3.place(x=150, y=40)

e4 = tk.Entry(root, textvariable=e4_var)
e4.place(x=150, y=140)

# Create a Text widget for displaying the list of books
text_box = tk.Text(root, height=20, width=60, state=tk.DISABLED)
text_box.place(x=400, y=100)

# Create search, filter, and sorting widgets
search_label = tk.Label(root, text="Search:", bg='green')
search_label.place(x=300, y=500)

search_entry = tk.Entry(root)
search_entry.place(x=350, y=500)

filter_label = tk.Label(root, text="Filter by Year:", bg='green')
filter_label.place(x=500, y=500)

filter_entry = tk.Entry(root)
filter_entry.place(x=600, y=500)

sort_label = tk.Label(root, text="Sort by:", bg='green')
sort_label.place(x=700, y=500)

# Combobox for sort options
sort_options = ["", "Title", "Author", "Year", "ISBN"]
sort_var = tk.StringVar(value="")
sort_combobox = ttk.Combobox(root, values=sort_options, textvariable=sort_var)
sort_combobox.place(x=750, y=500)

# Button to trigger the search, filter, and sorting
search_button = tk.Button(root, text="Search", bg="green", command=lambda: see_all_books(search_entry.get(), "", filter_entry.get(), sort_var.get(), "ASC"))
search_button.place(x=300, y=530)

# Create buttons for the application
view_all = tk.Button(root, text="View All", bg="green", command=lambda: see_all_books())
view_all.pack(padx=10, pady=3, side=tk.LEFT)


Add = tk.Button(root, text="Add Book", bg="green", command=lambda: insert(e1_var.get(), e3_var.get(), e2_var.get(), e4_var.get()))
Add.pack(padx=10, pady=3, side=tk.LEFT)

Delete = tk.Button(root, text="Delete", bg="green", command=delete_book)
Delete.pack(padx=10, pady=3, side=tk.LEFT)


Edit = tk.Button(root, text="Edit", bg="green", command=edit_book)
Edit.pack(padx=10, pady=3, side=tk.LEFT)

Quit = tk.Button(root, text="Quit", command=quit_application, bg="green")
Quit.pack(padx=10, pady=3, side=tk.LEFT)

# Start the Tkinter main loop
root.mainloop()

