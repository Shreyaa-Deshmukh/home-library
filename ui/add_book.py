import streamlit as st
from db.database import add_book
from services.openlibrary import fetch_book_details, search_isbn_by_title_author
from sample_test.barcode import scan_barcode
import os 

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



    # --- Option 2: Upload Barcode ---
    barcode_image = st.file_uploader("📷 Upload a barcode/QR code image", type=["png", "jpg", "jpeg"], key="barcode_upload")
    if barcode_image:
        os.makedirs("uploads", exist_ok=True)
        image_path = os.path.join("uploads", barcode_image.name)
        with open(image_path, "wb") as f:
            f.write(barcode_image.getbuffer())

        decoded = scan_barcode(image_path)
        if decoded:
            # ✅ Take first result & ensure it's a string
            isbn_candidate = str(decoded[0]).strip()

            if isbn_candidate.isdigit() and len(isbn_candidate) in (10, 13):
                st.info(f"Detected ISBN: {isbn_candidate} → adding to library...")
                title, author, _ = fetch_book_details(isbn_candidate)
                if title:
                    add_book(isbn_candidate, title, author, genre="Unknown", status="Available")
                    st.success(f"✅ Added: {title} by {author}")
                    st.session_state["menu"] = "View Library"
                    st.rerun()
                else:
                    st.warning("Could not fetch book details. Please add manually.")
            else:
                st.warning(f"Scanned code '{isbn_candidate}' is not a valid ISBN.")
        else:
            st.error("No barcode detected.")



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
            
