import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT,
                    title TEXT,
                    author TEXT,
                    genre TEXT,
                    status TEXT,
                    pdf_path TEXT
                )''')
    try:
        c.execute("ALTER TABLE books ADD COLUMN cover_path TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def add_book(isbn, title, author, genre, status="Available", pdf_path=None, cover_path=None):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (isbn, title, author, genre, status, pdf_path, cover_path) VALUES (?,?,?,?,?,?,?)",
              (isbn, title, author, genre, status, pdf_path, cover_path))
    conn.commit()
    conn.close()


def get_all_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    results = c.fetchall()
    conn.close()
    return results

def get_book_by_id(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE id=?", (book_id,))
    result = c.fetchone()
    conn.close()
    return result

def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def update_pdf(book_id, pdf_path):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET pdf_path=? WHERE id=?", (pdf_path, book_id))
    conn.commit()
    conn.close()

def update_cover(book_id, cover_path):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET cover_path=? WHERE id=?", (cover_path, book_id))
    conn.commit()
    conn.close()

# (same pattern for get_all_books, get_book_by_id, delete_book, update_pdf, update_cover)
