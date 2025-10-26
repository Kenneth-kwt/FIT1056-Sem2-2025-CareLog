import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import load_data

from services.staff_service import register_staff

CARELOG_FILE = "data/careLog.json"

def register_staff_form():
    """Display the staff registration form and handle submission."""
    
    data = load_data(CARELOG_FILE)
    next_user_id = data.get("next_user_id", 1)

    st.header("Register New Staff Member")

    with st.form("staff_register_form"):
        user_id = st.text_input("User ID", value=next_user_id, disabled=True)
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        speciality = st.text_input("Speciality (e.g., Doctor, Nurse)")

        submitted = st.form_submit_button("Register Staff")

        if submitted:
            if not user_id or not password or not name or not speciality:
                st.error("All fields are required.")
            else:
                staff = register_staff(user_id, password,speciality,name)
            if staff:
                st.success(f"Staff '{name}' registered successfully!")
            else:
                st.error("Registration failed — user may already exist.")