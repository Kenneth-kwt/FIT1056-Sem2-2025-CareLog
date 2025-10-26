import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import load_data

from services.user_service import delete_user

def delete_user_form():
    """Display the user deletion form and handle submission."""
    st.header("Delete User Record")

    user_id = st.text_input("Enter User ID to delete")
    if st.button("Delete User"):
        if delete_user(user_id):
            st.success(f"User '{user_id}' deleted successfully.")
        else:
            st.error("User not found or could not be deleted.")
