import streamlit as st

def show_welcome():
    # Title + spacing
    st.title("📚 Welcome to Home Library Manager")
    st.subheader("Your personal digital bookshelf")

    st.markdown(
        """
        Manage your personal library with ease:  
        - ➕ Add books by ISBN, barcode, or manually  
        - 🖼️ Upload covers and PDFs  
        - 📖 Browse and search your collection  
        - 🔍 Access details instantly with QR codes
        """,
        unsafe_allow_html=False,
    )

    # Add some spacing before buttons
    st.markdown("---")
    st.write("")
    st.write("### 🚀 Get Started")

    # Center the buttons using columns
    col1, col2, col3 = st.columns([1, 2, 1])  # middle column wider
    with col2:
        if st.button("➕ Add Book", use_container_width=True):
            st.session_state["menu"] = "Add Book"
            st.rerun()
        st.write("")  # small gap
        if st.button("📚 View Library", use_container_width=True):
            st.session_state["menu"] = "View Library"
            st.rerun()
