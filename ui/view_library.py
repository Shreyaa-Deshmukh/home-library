import streamlit as st
from db.database import get_all_books, delete_book
from utils.helper import get_cover_url

def show_view_library(book_card_template):
    st.subheader("📖 Your Bookshelf")

    books = get_all_books()
    if not books:
        st.info("No books yet.")
    else:
        for row_start in range(0, len(books), 4):
            cols = st.columns(4)
            for i, b in enumerate(books[row_start:row_start+4]):
                with cols[i]:
                    cover_url = get_cover_url(b[1], b[7])

                    if cover_url.startswith("uploads/"):
                        # Local uploaded cover → show with Streamlit
                        st.image(cover_url, width=150)
                        st.markdown(f"**{b[2]}**  \n*{b[3]}*")
                    else:
                        # Remote cover → use HTML template
                        card_html = book_card_template.replace("{{cover_url}}", cover_url) \
                                                     .replace("{{title}}", b[2]) \
                                                     .replace("{{author}}", b[3])
                        st.markdown(card_html, unsafe_allow_html=True)

                    # Buttons
                    col1, col2 = st.columns(2)
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

