# main_dashboard.py - Main Streamlit Application
import streamlit as st
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from services.patient_services import register_patient, add_patient_log, delete_patient
from utils.storage import load_data

CARELOG_FILE = "data/careLog.json"
=======
from services.user_service import login, add_user, delete_user
from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import add_staff_log, view_patient_history
>>>>>>> Stashed changes

st.set_page_config(page_title="CareLog System", layout="wide")


# MAIN FUNCTION
def launch():
<<<<<<< Updated upstream
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
=======
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
                    st.error("ERROR: Invalid credentials")

        st.stop()  # prevent showing main UI before login

    # --- Top Navigation Bar ---
    user = st.session_state.user
    st.sidebar.title(f"Welcome, {user.user_id}!")
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
        st.header("Register New Patient")
>>>>>>> Stashed changes

        with st.form("register_form"):
            user_id = st.text_input("User ID")
            password = st.text_input("Password", type="password")
<<<<<<< Updated upstream
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
=======
    st.title("CareLog System")
    st.sidebar.title("Navigation")

    # Login Section
    if "user" not in st.session_state:
        st.subheader("Please Login")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(user_id, password)
            if user:
                st.session_state.user = user.to_dict()
                st.success(f"Welcome, {user_id}!")
            else:
                st.error("Invalid credentials. Please try again.")
        return  # stop here if not logged in

    # After Login
    user = st.session_state.user
    role = user["role"]

    st.sidebar.markdown(f"**Logged in as:** {user['user_id']} ({role})")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.experimental_rerun()

    # ROUTE BY ROLE
    if role == "patient":
        patient_dashboard()
    elif role == "staff":
        staff_dashboard()
    elif role == "admin":
        admin_dashboard()
    else:
        st.warning("Unknown role. Contact administrator.")

# PATIENT DASHBOARD
def patient_dashboard():
    st.header("Patient Dashboard")
    page = st.sidebar.radio("Select Section", ["Register", "Add Log", "Delete Account"])

    if page == "Register":
        st.subheader("Register New Patient")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        ailment = st.text_input("Ailment / Condition")
        culture = st.text_input("Culture & Religion")

        if st.button("Register Patient"):
            result = register_patient(user_id, password, name, age, gender, ailment, culture)
            if result:
                st.success("Registered successfully!")
                st.json(result.to_dict())
            else:
                st.error("ERROR: User already exists or registration failed.")

    elif page == "Add Log":
        st.subheader("Add Daily Log")
        user_id = st.text_input("Patient User ID")
        mood = st.selectbox("Mood", ["Happy", "Sad", "Neutral", "Anxious", "Angry", "Tired", "Other"])
        pain_level = st.slider("Pain Level (0–10)", 0, 10, 5)
        notes = st.text_area("Notes")
        sensitive = st.checkbox("Contains sensitive info")

        if st.button("Add Log"):
            patient = add_patient_log(user_id, mood, pain_level, notes, sensitive)
            if patient:
                st.success("Log added successfully.")
                st.json(patient.to_dict())
            else:
                st.error("ERROR: Patient not found.")

    elif page == "Delete Account":
        st.subheader("ERROR: Delete Patient")
        user_id = st.text_input("Patient User ID to Delete")
        if st.button("Delete Patient"):
            success = delete_patient(user_id)
            if success:
                st.success("Patient deleted successfully!")
            else:
                st.error("ERROR: Could not delete patient.")

# STAFF DASHBOARD
def staff_dashboard():
    st.header("Staff Dashboard")
    page = st.sidebar.radio("Select Section", ["Add Log for Patient", "View Patient History"])

    if page == "Add Log for Patient":
        st.subheader("🩺 Add Patient Log")
        staff_id = st.text_input("Staff ID")
        patient_name = st.text_input("Patient Name")
        patient_symptoms = st.text_area("Symptoms")
        diagnosis = st.text_input("Diagnosis")
        prescription = st.text_area("Prescription")
        notes = st.text_area("Notes")

        if st.button("Add Staff Log"):
            result = add_staff_log(
                staff_id=staff_id,
                patient_name=patient_name,
                patient_symptoms=patient_symptoms,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes,
            )
            if result:
                st.success("Staff log added successfully!")
            else:
                st.error("ERROR: Failed to add log. Check staff-patient assignment.")

    elif page == "View Patient History":
        st.subheader("View Patient History")
        patient_id = st.text_input("Patient ID")
        if st.button("View History"):
            history = view_patient_history(patient_id)
            if history:
                st.json(history)
            else:
                st.warning("No patient history found.")

# ADMIN DASHBOARD
def admin_dashboard():
    st.header("Admin Dashboard")
    page = st.sidebar.radio("Select Section", ["Add User", "Delete User"])

    if page == "Add User":
        st.subheader("Add New User")
        new_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["patient", "staff", "admin"])

        if st.button("Add User"):
            user = add_user(new_id, password, role)
            if user:
                st.success("User added successfully!")
            else:
                st.error("ERROR: User already exists.")

    elif page == "Delete User":
        st.subheader("Delete User")
        del_id = st.text_input("User ID to delete")
        if st.button("Delete User"):
            if delete_user(del_id):
                st.success("User deleted.")
            else:
                st.error("ERRR: User not found.")

>>>>>>> Stashed changes
=======
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
                    st.error("ERROR: Registration failed — user may already exist.")

    # ---- Delete Patient ----
    elif page == "Delete Patient":
        st.header("Delete Patient Record")

        user_id = st.text_input("Enter Patient User ID to delete")
        if st.button("Delete Patient"):
            if delete_patient(user_id):
                st.success(f"Patient '{user_id}' deleted successfully.")
            else:
                st.error("ERROR: Patient not found or could not be deleted.")

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
            st.warning("ERROR: No patients found in the system.")

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
                    st.error("ERROR: Staff not found or patient not assigned!")

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
                st.error("ERROR: Patient not found or no history available.")

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
                    st.error("ERROR: Could not find your patient record.")

    # ---- View My Logs (Patient) ----
    elif page == "View My Logs":
        st.header("🩺 My Logs")

        data = load_data(CARELOG_FILE)
        patients = data.get("patients", [])
        my_data = next((p for p in patients if p["user_id"] == user.user_id), None)

        if my_data:
            logs = my_data.get("logs", [])
            if logs:
                for log in logs:
                    st.markdown(
                        f"- 🕒 {log.get('timestamp', 'N/A')} | "
                        f"Mood: {log.get('mood', 'N/A')} | "
                        f"Pain: {log.get('pain_level', 'N/A')} | "
                        f"Notes: {log.get('notes', '')}"
                    )
            else:
                st.info("No logs recorded yet.")
        else:
            st.error("ERROR: Your patient record was not found.")


>>>>>>> Stashed changes
