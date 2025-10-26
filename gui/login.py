import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import login
from services.patient_service import register_patient
from gui.config_patient import patient_register_form
from gui.config_staff import register_staff_form


def show_login_page():
    """Display the login and registration interface with sidebar navigation."""
    st.sidebar.title("CareLog System")
    page = st.sidebar.radio("Navigation", ["Login", "Register"])

    if page == "Login":
        st.title("CareLog System Login")
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

    elif page == "Register":
        st.title("Register for CareLog")
        st.markdown("Choose your registration type below:")

        tab1, tab2 = st.tabs(["Patient Registration", "Staff Registration"])

        with tab1:
            patient_register_form()

        with tab2:
            register_staff_form()

    st.stop()  # Prevent main dashboard from showing until login
