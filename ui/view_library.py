import streamlit as st
from db.database import get_all_books, delete_book
from utils.helper import get_cover_url



def show_view_library(book_card_template):
    st.subheader("📖 Your Bookshelf")

    col1, col2 = st.columns([3,1])
    with col1:
    # 🔎 Add search bar
        search_query = st.text_input("🔍 Search books by title or author", key="search_box")
    with col2 :
        sort_option = st.selectbox("Sort by:",["Recent","Title"], index=0)
    books = get_all_books()

    # Filter books based on search query
    if search_query:
        books = [
            b for b in books
            if search_query.lower() in b[2].lower()  # title
            or search_query.lower() in b[3].lower()  # author
        ]

    #---Apply Sorting---
    if sort_option == "Title":
        books.sort(key=lambda b : b[2].lower())
    else:
        books.sort(key=lambda b:b[0], reverse=True)
    
    #---Display books---
    if not books:
        st.info("No books found." if search_query else "No books yet.")
    else:
        for row_start in range(0, len(books), 4):
            cols = st.columns(4)
            for i, b in enumerate(books[row_start:row_start+4]):
                with cols[i]:
                    cover_url = get_cover_url(b[1], b[7])

                    if cover_url.startswith("uploads/"):
                        st.image(cover_url, width=150)
                        st.markdown(f"**{b[2]}**  \n*{b[3]}*")
                    else:
                        card_html = book_card_template.replace("{{cover_url}}", cover_url) \
                                                     .replace("{{title}}", b[2]) \
                                                     .replace("{{author}}", b[3])
                        st.markdown(card_html, unsafe_allow_html=True)

                    # Buttons
                    col1, col2= st.columns(2)
                    with col1:
                        if st.button("View", key=f"view_{b[0]}"):
                            st.session_state["selected_book"] = b[0]
                            st.session_state["menu"] = "Book Details"
                            st.rerun()
                    with col2:
                        if st.button("❌ Delete", key=f"delete_{b[0]}"):
                            delete_book(b[0])
                            st.warning(f"Deleted {b[2]}")
                            st.rerun()
