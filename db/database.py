import sqlite3
import uuid
import csv
import os

DB_PATH = "library.db"
CSV_PATH = "library.csv"

def init_db():
    conn = sqlite3.connect(DB_PATH) #open connection
    c = conn.cursor() #calls connection
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT,
                    title TEXT,
                    author TEXT,
                    genre TEXT,
                    status TEXT,
                    pdf_path TEXT,
                    cover_path TEXT,
                    accessible_number TEXT UNIQUE
                )''')
    try:
        c.execute("ALTER TABLE books ADD COLUMN accessible_number TEXT UNIQUE")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    sync_to_csv()

def sync_to_csv():
    """Export the entire books table to library.csv"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    headers = [desc[0] for desc in c.description]  # column names

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()   


def generate_accessible_number():
    """Generate next available unique number like HL-0001, HL-0002 ..."""
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    conn.close()
    return f"HL-{count+1:04d}"

def add_book(isbn, title, author, genre, status="Available", pdf_path=None, cover_path=None):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
  
    
    # ✅ Check if book already exists by ISBN
    c.execute("SELECT id FROM books WHERE isbn=? AND title=? AND author=?", (isbn, title, author))
    existing = c.fetchone()
    if existing:
        conn.close()
        return False   # 🚨 Duplicate found

    accessible_number = str(uuid.uuid4())[:8]
    c.execute("INSERT INTO books (isbn, title, author, genre, status, pdf_path, cover_path, accessible_number ) VALUES (?,?,?,?,?,?,?,?)",
              (isbn, title, author, genre, status, pdf_path, cover_path, accessible_number))
    conn.commit()
    conn.close()
    sync_to_csv()


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

def get_book_by_accessible_number(accessible_number):
    """Fetch book using its unique accessible number (used by QR code scanning)"""
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE accessible_number=?", (accessible_number,))
    result = c.fetchone()
    conn.close()
    return result

def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    sync_to_csv()

def update_pdf(book_id, pdf_path):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET pdf_path=? WHERE id=?", (pdf_path, book_id))
    conn.commit()
    conn.close()
    sync_to_csv()

def update_cover(book_id, cover_path):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET cover_path=? WHERE id=?", (cover_path, book_id))
    conn.commit()
    conn.close()
    sync_to_csv()

# (same pattern for get_all_books, get_book_by_id, delete_book, update_pdf, update_cover)
