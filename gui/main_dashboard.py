import streamlit as st
from services.patient_services import register_patient, add_patient_log, delete_patient
from services.staff_service import add_staff_log, view_patient_history
from services.user_service import login, seed_users
from utils.storage import load_data
from app.log import logManager

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
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")

        st.stop()  # prevent showing main UI before login

    # --- Top Navigation Bar ---
    user = st.session_state.user
    st.sidebar.title(f"Welcome, {user.user_id}")
    st.sidebar.caption(f"Role: {user.role}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

    # --- Navigation Menu (based on role) ---
    if user.role == "admin":
        pages = [
            "Register Patient",
            "Delete Patient",
            "View All Patients",
            "Add Staff Log",
            "View Patient History"
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
        st.header("🩺 Register New Patient")

        with st.form("register_form"):
            user_id = st.text_input("User ID")
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

    # ---- Delete Patient ----
    elif page == "Delete Patient":
        st.header("🗑️ Delete Patient Record")

        user_id = st.text_input("Enter Patient User ID to delete")
        if st.button("Delete Patient"):
            if delete_patient(user_id):
                st.success(f"Patient '{user_id}' deleted successfully.")
            else:
                st.error("Patient not found or could not be deleted.")

    # ---- View All Patients ----
    elif page == "View All Patients":
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
        st.header("View Patient Full History")

        patient_id = st.text_input("Enter Patient User ID")

        if st.button("View History"):
            history = view_patient_history(patient_id)
            if history:
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
                st.error("Patient not found or no history available.")

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




