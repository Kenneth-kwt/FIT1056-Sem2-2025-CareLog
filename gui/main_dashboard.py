import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import add_staff_log, view_patient_history
from services.user_service import login, seed_users
from utils.storage import load_data

from gui.login import show_login_page
from gui.config_patient import (
    patient_register_form,
    view_all_patients,
    view_patient_history_page,
    assign_staff_to_patient_form
)
from gui.config_general import delete_user_form

CARELOG_FILE = "data/careLog.json"

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="CareLog System")

    # Ensure initial users exist
    seed_users()

    # --- Session State Setup ---
    if "user" not in st.session_state:
        st.session_state.user = None

    # --- Login Page ---
    if not st.session_state.user:
        show_login_page()

    # --- Top Navigation Bar ---
    user = st.session_state.user
    st.sidebar.title(f"Welcome, {user.user_id}")
    st.sidebar.caption(f"Role: {user.role}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    # --- Navigation Menu (based on role) ---
    if user.role == "admin":
        pages = [
            "Register Patient",
            "Register Staff",
            "Delete User",
            "View All Patients",
            "Add Staff Log",
            "View Patient History",
            "Assign Staff to Patient"
        ]
    elif user.role == "staff":
        pages = ["Add Staff Log", "View Patient History"]
    elif user.role == "patient":
        pages = ["Add Patient Log", "View My Logs"]
    else:
        st.error("Unknown role detected.")
        return

    page = st.sidebar.radio("Navigate", pages)

    # ================= ADMIN / STAFF / PATIENT INTERFACES =================
    # ---- Register Patient ----
    if page == "Register Patient":
        patient_register_form()

    # ---- Delete User ----
    elif page == "Delete User":
        delete_user_form()

    # ---- View All Patients ----
    elif page == "View All Patients":
        view_all_patients()

    # ---- Add Staff Log ----
    elif page == "Add Staff Log":
        st.header("Add Staff Log Entry")

        with st.form("staff_log_form"):
            staff_id = user.user_id if user.role == "staff" else st.text_input("Staff User ID")
            patient_name = st.text_input("Patient Name")
            patient_symptoms = st.text_input("Patient Symptoms")
            patient_log_timestamp = st.text_input("Patient Log Timestamp (optional)")
            diagnosis = st.text_area("Diagnosis")
            prescription = st.text_area("Prescription / Treatment Plan")
            notes = st.text_area("Additional Notes")
            patient_logs = st.text_area("Summary of Patient Logs (optional)")

            submitted = st.form_submit_button("Add Staff Log")

            if submitted:
                staff = add_staff_log(
                    staff_id,
                    patient_name=patient_name,
                    patient_symptoms=patient_symptoms,
                    patient_log_timestamp=patient_log_timestamp,
                    diagnosis=diagnosis,
                    prescription=prescription,
                    notes=notes,
                    patient_logs=patient_logs,
                )

                if staff:
                    st.success(f"Log added successfully for staff '{staff_id}' and patient '{patient_name}'")
                else:
                    st.error("Staff not found or patient not assigned!")

    # ---- View Patient History ----
    elif page == "View Patient History":
        view_patient_history_page()

    ## ---- Assign Staff to Patient ----
    elif page == "Assign Staff to Patient":
        assign_staff_to_patient_form()

    # ---- Add Patient Log ----
    elif page == "Add Patient Log":
        st.header("Add Your Own Log")

        with st.form("log_form"):
            mood = st.text_input("Mood (e.g., Happy, Anxious, Calm)")
            pain_level = st.slider("Pain Level (0 = None, 10 = Extreme)", 0, 10, 5)
            notes = st.text_area("Notes")
            sensitive_information = st.checkbox("Mark as sensitive", value=False)

            submitted = st.form_submit_button("Add Log Entry")

            if submitted:
                patient = add_patient_log(user.user_id, mood, pain_level, notes, sensitive_information)
                if patient:
                    st.success("Log entry added successfully!")
                else:
                    st.error("Could not find your patient record.")

    # ---- View My Logs (Patient) ----
    elif page == "View My Logs":
        st.header("My Logs")

        data = load_data(CARELOG_FILE)
        patients = data.get("patients", [])
        my_data = next((p for p in patients if p["user_id"] == user.user_id), None)

        if my_data:
            logs = my_data.get("logs", [])
            if logs:
                for log in logs:
                    st.markdown(
                        f"- {log.get('timestamp', 'N/A')} | "
                        f"Mood: {log.get('mood', 'N/A')} | "
                        f"Pain: {log.get('pain_level', 'N/A')} | "
                        f"Notes: {log.get('notes', '')}"
                    )
            else:
                st.info("No logs recorded yet.")
        else:
            st.error("Your patient record was not found.")
