# gui/main_dashboard.py
import streamlit as st
from services.patient_services import register_patient, add_patient_log, delete_patient
from utils.storage import load_data

CARELOG_FILE = "data/careLog.json"

def launch():
    """Main Streamlit dashboard for CareLog System."""
    st.set_page_config(layout="wide", page_title="CareLog System")

    # --- App Title ---
    st.title(" CareLog Patient Management System")

    # --- Sidebar Navigation ---
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Register Patient", "Add Patient Log", "View Patients", "Delete Patient"]
    )

    if page == "Register Patient":
        st.subheader("Register a New Patient")

        with st.form("register_form"):
            user_id = st.text_input("User ID")
            password = st.text_input("Password", type="password")
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            ailment = st.text_input("Ailment / Condition")
            culture_and_religion = st.text_input("Culture & Religion")
            submitted = st.form_submit_button("Register Patient")

        if submitted:
            patient = register_patient(user_id, password, name, age, gender, ailment, culture_and_religion)
            if patient:
                st.success(f"Registered patient '{name}' successfully!")
            else:
                st.error("User already exists!")
    elif page == "Add Patient Log":
        st.subheader("Add a Patient Log Entry")

        with st.form("log_form"):
            user_id = st.text_input("Patient User ID")
            mood = st.selectbox("Mood", ["Happy", "Neutral", "Sad", "Anxious", "Angry", "None"])
            pain_level = st.slider("Pain Level", 0, 10, 5)
            notes = st.text_area("Notes")
            sensitive = st.checkbox("Sensitive Information")
            submit_log = st.form_submit_button("Add Log")

        if submit_log:
            patient = add_patient_log(user_id, mood, pain_level, notes, sensitive)
            if patient:
                st.success(f"Log added successfully for patient '{user_id}'.")
            else:
                st.error("Patient not found.")
    elif page == "View Patients":
        st.subheader("All Registered Patients")

        data = load_data(CARELOG_FILE)
        patients = data.get("patients", [])

        if not patients:
            st.info("No patients registered yet.")
        else:
            for p in patients:
                with st.expander(f"{p['name']} (ID: {p['user_id']})"):
                    st.write(f"**Age:** {p['age']}")
                    st.write(f"**Gender:** {p['gender']}")
                    st.write(f"**Ailment:** {p['ailment']}")
                    st.write(f"**Culture & Religion:** {p['culture_and_religion']}")

                    st.markdown("**Logs:**")
                    logs = p.get("logs", [])
                    if not logs:
                        st.write("_No logs yet._")
                    else:
                        for log in logs:
                            st.markdown(
                                f"- **Mood:** {log['mood']}, "
                                f"**Pain:** {log['pain_level']}, "
                                f"**Notes:** {log['notes']}"
                            )
    elif page == "Delete Patient":
        st.subheader("Delete a Patient Record")

        user_id = st.text_input("Enter the Patient's User ID")
        if st.button("Delete Patient"):
            if delete_patient(user_id):
                st.success(f"Deleted patient '{user_id}' successfully.")
            else:
                st.error("ERROR: Patient not found or could not be deleted.")
