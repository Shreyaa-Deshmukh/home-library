import streamlit as st
from db.database import init_db, get_book_by_accessible_number
from ui.add_book import show_add_book
from ui.view_library import show_view_library
from ui.book_details import show_book_details
from ui.welcome import show_welcome


def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_html_template(file_name):
    with open(file_name, "r") as f:
        return f.read()

def main():
    st.set_page_config(page_title="Home Library Manager", layout="wide")

    # Load external assets
    load_css("static/styles.css")
    book_card_template = load_html_template("static/book_card.html")

    # ✅ Handle QR param scan
    query_params = st.query_params
    if "book" in query_params:
        accessible_number = query_params["book"]
        book = get_book_by_accessible_number(accessible_number)
        if book:
            st.session_state["selected_book"] = book[0]  # book id
            st.session_state["menu"] = "Book Details"

    # ✅ Default landing page = Welcome
    if "menu" not in st.session_state:
        st.session_state["menu"] = "Welcome"

    # --- Routing ---
    if st.session_state["menu"] == "Welcome":
        show_welcome()
    else:
        # Sidebar navigation (only visible after Welcome)
        menu = ["Welcome", "Add Book", "View Library", "Book Details"]
        choice = st.sidebar.radio("Menu", menu, index=menu.index(st.session_state["menu"]))

        if choice != st.session_state["menu"]:
            st.session_state["menu"] = choice

        if st.session_state["menu"] == "Add Book":
            show_add_book()
        elif st.session_state["menu"] == "View Library":
            show_view_library(book_card_template)
        elif st.session_state["menu"] == "Book Details":
            show_book_details()
        elif st.session_state["menu"] == "Welcome":
            show_welcome()  # allow coming back home

if __name__ == "__main__":
    init_db()
    main()
