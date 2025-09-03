import os
import streamlit as st
import qrcode
from db.database import get_book_by_id, update_cover, update_pdf
from services.openlibrary import fetch_book_details, get_cover_url


def generate_qr_for_book(accessible_number, book_id):
    """Generate and cache QR code for a book."""
    os.makedirs("uploads", exist_ok=True)
    qr_path = os.path.join("uploads", f"qr_{book_id}.png")
    if not os.path.exists(qr_path):  # generate once, reuse later
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(f"http://localhost:8501?book={accessible_number}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)
    return qr_path

def show_book_details():
    st.subheader("📖 Book Details")
    if "selected_book" not in st.session_state:
        st.info("Go to 'View Library' and select a book.")
        return

    book_id = st.session_state["selected_book"]
    book = get_book_by_id(book_id)

    if not book:
        st.error("Book not found.")
        return

    # Show cover + details
    st.image(get_cover_url(book[1], book[7]), width=200)
    st.subheader(book[2])
    st.write(f"**Author:** {book[3]}")
    st.write(f"**Genre:** {book[4]}")
    st.write(f"**Status:** {book[5]}")

    if len(book) >= 9  and book[8] :
        qr_path = generate_qr_for_book(book[8], book_id)
        st.markdown("**Share this book:**")
        st.image(qr_path, width=150, caption=f"Scan to view {book[2]}")


    # If book has ISBN → try preview from OpenLibrary
    if book[1] != "Manual":
        _, _, preview_url = fetch_book_details(book[1])
        if preview_url:
            st.markdown(f"[📖 Read Online / Borrow]({preview_url})", unsafe_allow_html=True)
        else:
            st.warning("No online version available.")
    else:
        st.info("Manual entry – no online preview available.")

        # --- Upload custom cover ---
        cover_file = st.file_uploader("Upload a custom cover", type=["png", "jpg", "jpeg"], key=f"cover_{book_id}")
        if cover_file:
            os.makedirs("uploads", exist_ok=True)
            cover_path = os.path.join("uploads", f"cover_{book_id}.png")
            with open(cover_path, "wb") as f:
                f.write(cover_file.getbuffer())
            update_cover(book_id, cover_path)
            st.success("✅ Custom cover uploaded!")
            st.session_state["menu"] = "View Library"
            st.rerun()

        # --- Upload PDF ---
        pdf_file = st.file_uploader("Upload book PDF", type=["pdf"], key=f"pdf_{book_id}")
        if pdf_file:
            os.makedirs("uploads", exist_ok=True)
            pdf_path = os.path.join("uploads", f"book_{book_id}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            update_pdf(book_id, pdf_path)
            st.success("✅ PDF uploaded successfully!")
            st.session_state["menu"] = "View Library"
            st.rerun()

    # --- If PDF already exists, allow reading ---
    if book[6]:
        with open(book[6], "rb") as f:
            st.download_button("📖 Read Book", f, file_name=os.path.basename(book[6]))
