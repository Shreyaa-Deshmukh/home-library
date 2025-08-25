import streamlit as st
from db.database import init_db
from ui.add_book import show_add_book
from ui.view_library import show_view_library
from ui.book_details import show_book_details

def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_html_template(file_name):
    with open(file_name, "r") as f:
        return f.read()

def main():
    st.set_page_config(page_title="Home Library Manager", layout="wide")
    st.title("📚 Home Library Manager")

    load_css("static/styles.css")
    book_card_template = load_html_template("static/book_card.html")

    if "menu" not in st.session_state:
        st.session_state["menu"] = "View Library"

    menu = ["Add Book", "View Library", "Book Details"]
    choice = st.sidebar.radio("Menu", menu, index=menu.index(st.session_state["menu"]))

    if choice == "Add Book":
        show_add_book()
    elif choice == "View Library":
        show_view_library(book_card_template)
    elif choice == "Book Details":
        show_book_details()

if __name__ == "__main__":
    init_db()
    main()


