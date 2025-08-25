import streamlit as st
from db.database import add_book
from services.openlibrary import fetch_book_details, search_isbn_by_title_author

def show_add_book():
    st.subheader("➕ Add Book")
    isbn = st.text_input("Enter ISBN")
    if st.button("Fetch Details"):
        if isbn.strip() =="":
            st.warning("Please Enter ISBN")
        else:    
            title, author, _ = fetch_book_details(isbn)
            if title:
                add_book(isbn, title, author, genre="Unknown", status="Available")
                st.success(f"✅ Added: {title} by {author}")   # <-- show here    
            else:
                st.error("No details found. Try manual entry.")

    st.write("Or enter manually:")
    manual_title = st.text_input("Title")
    manual_author = st.text_input("Author")
    manual_genre = st.text_input("Genre")
    if st.button("Add Manual Book"):
        if manual_title.strip():
            isbn_guess = search_isbn_by_title_author(manual_title, manual_author)
            if isbn_guess:
                title, author, _ = fetch_book_details(isbn_guess)
                if title:
                    add_book(isbn_guess, title, author, manual_genre)
                    st.success(f"✅ Added: {title} by {author}")
                else:
                    add_book("Manual", manual_title, manual_author, manual_genre)
                    st.success(f"✅ Added: {manual_title} by {manual_author}")
            else:
                add_book("Manual", manual_title, manual_author, manual_genre)
                st.success(f"✅ Added: {manual_title} by {manual_author}")
            
