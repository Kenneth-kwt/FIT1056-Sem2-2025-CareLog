import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import login

def show_login_page():
    """Display the login page and handle user authentication."""
    st.title("🔐 CareLog System Login")
    st.markdown("Please sign in to access the system.")
    with st.form("login_form"):
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = login(user_id, password)
            if user:
                st.session_state.user = user
                st.success(f"Logged in as {user.user_id} ({user.role})")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()  # prevent showing main UI before login