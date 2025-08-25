import requests, os

def fetch_book_details(isbn):
    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(url, timeout=10).json()
        key = f"ISBN:{isbn}"
        if key in response:
            book = response[key]
            title = book.get("title", "Unknown")
            authors = book.get("authors", [])
            author = ", ".join([a.get("name", "Unknown") for a in authors]) if authors else "Unknown"
            preview_url = book.get("url", None)
            return title, author, preview_url
    except:
        return None, None, None
    return None, None, None

def search_isbn_by_title_author(title, author):
    try:
        url = f"https://openlibrary.org/search.json?title={title}&author={author}&limit=1"
        response = requests.get(url, timeout=10).json()
        if response.get("docs"):
            doc = response["docs"][0]
            if "isbn" in doc:
                return doc["isbn"][0]
    except:
        return None
    return None

def get_cover_url(isbn, cover_path):
    if cover_path and os.path.exists(cover_path):
        return cover_path
    elif isbn and isbn != "Manual":
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    else:
        return "https://via.placeholder.com/150x200.png?text=No+Cover"
