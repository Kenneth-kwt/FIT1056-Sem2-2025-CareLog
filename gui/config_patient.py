import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import load_data

from services.patient_service import register_patient, delete_patient
from services.admin_service import assign_staff_to_patient
from services.staff_service import add_staff_log, view_patient_history

CARELOG_FILE = "data/careLog.json"

def patient_register_form():
    """Display the patient registration form and handle submission."""

    data = load_data(CARELOG_FILE)
    next_user_id = data.get("next_user_id", 1)

    st.header("Register New Patient")

    with st.form("register_form"):
        user_id = st.text_input("User ID", value=next_user_id, disabled=True)
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        ailment = st.text_input("Ailment / Condition")
        culture_and_religion = st.text_input("Culture and Religion")

        submitted = st.form_submit_button("Register Patient")

        if submitted:
            patient = register_patient(user_id, password, name, age, gender, ailment, culture_and_religion)
            if patient:
                st.success(f"Patient '{name}' registered successfully!")
            else:
                st.error("Registration failed — user may already exist.")

def view_all_patients():
    """Display a list of all registered patients."""
    st.header("View All Registered Patients")

    data = load_data(CARELOG_FILE)
    if "patients" in data and data["patients"]:
        for p in data["patients"]:
            with st.expander(f"{p.get('name', 'Unknown')} ({p.get('user_id')})"):
                st.write(f"**Age:** {p.get('age')}")
                st.write(f"**Gender:** {p.get('gender')}")
                st.write(f"**Ailment:** {p.get('ailment')}")
                st.write(f"**Culture & Religion:** {p.get('culture_and_religion')}")
                st.write("**Logs:**")
                logs = p.get("logs", [])
                if logs:
                    for log in logs:
                        st.markdown(
                            f"- *{log.get('timestamp', 'No Time')}*: "
                            f"Mood: **{log.get('mood', 'N/A')}**, "
                            f"Pain: {log.get('pain_level', 'N/A')}, "
                            f"Notes: {log.get('notes', '')}"
                        )
                else:
                    st.info("No logs recorded yet.")
    else:
        st.warning("No patients found in the system.")

def view_patient_history_page():
    """Display the history of a specific patient."""
    user = st.session_state.user
    st.header("View Patient Full History")

    patient_id = st.text_input("Enter Patient User ID")

    if st.button("View History"):
        status, history = view_patient_history(patient_id, user.user_id)
        if status:
            st.subheader("Patient Details")
            st.write(f"**Ailment:** {history['patient_ailment']}")
            st.write("**Patient Logs:**")
            for log in history["patient_logs"]:
                st.markdown(
                    f"- {log.get('timestamp', 'N/A')}: Mood {log.get('mood', 'N/A')}, "
                    f"Pain {log.get('pain_level', 'N/A')} — {log.get('notes', '')}"
                )
            st.write("**Staff Logs:**")
            for staff_name, logs in history["staff_logs"].items():
                st.markdown(f"**{staff_name}**")
                for log in logs:
                    st.markdown(
                        f"   - Diagnosis: {log.get('diagnosis', 'N/A')}, "
                        f"Prescription: {log.get('prescription', 'N/A')}, "
                        f"Notes: {log.get('notes', '')}"
                    )
        else:
            st.warning(history)

def assign_staff_to_patient_form():
    """Display the form to assign staff to a patient."""
    st.header("Assign Staff to Patient")

    patient_id = st.text_input("Enter Patient User ID")
    staff_id = st.text_input("Enter Staff User ID to assign")

    if st.button("Assign Staff"):
        if assign_staff_to_patient(patient_id, staff_id):
            st.success(f"Staff '{staff_id}' assigned to patient '{patient_id}' successfully.")
        else:
            st.error("Assignment failed — patient not found or staff already assigned.")
