import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import load_data

from services.patient_service import register_patient, delete_patient,patient_bill
from services.admin_service import assign_staff_to_patient,view_patient_history_admin
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

# def view_patient_history_page():
#     """Display the history of a specific patient."""
#     user = st.session_state.user
#     st.header("View Patient Full History")

#     patient_id = st.text_input("Enter Patient User ID")

#     if st.button("View History"):
#         status, history = view_patient_history(patient_id, user.user_id)
#         if status:
#             st.subheader("Patient Details")
#             st.write(f"**Ailment:** {history['patient_ailment']}")
#             st.write("**Patient Logs:**")
#             for log in history["patient_logs"]:
#                 st.markdown(
#                     f"- {log.get('timestamp', 'N/A')}: Mood {log.get('mood', 'N/A')}, "
#                     f"Pain {log.get('pain_level', 'N/A')} — {log.get('notes', '')}"
#                 )
#             st.write("**Staff Logs:**")
#             for staff_name, logs in history["staff_logs"].items():
#                 st.markdown(f"**{staff_name}**")
#                 for log in logs:
#                     st.markdown(
#                         f"   - Diagnosis: {log.get('diagnosis', 'N/A')}, "
#                         f"Prescription: {log.get('prescription', 'N/A')}, "
#                         f"Notes: {log.get('notes', '')}"
#                     )
#         else:
#             st.warning(history)

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

            # --- Patient Logs ---
            st.write("### Patient Logs")
            patient_logs = history.get("patient_logs", [])
            if patient_logs:
                for log in patient_logs:
                    timestamp = log.get('timestamp', 'N/A')
                    sensitive = log.get("sensitive_information", False)
                    expander_label = f"{'Sensitive Log - ' if sensitive else ''}{timestamp}"

                    with st.expander(expander_label, expanded=False):
                        if sensitive:
                            st.warning("This entry contains sensitive information. Viewer discretion is advised.")
                        st.markdown(
                            f"- Mood: {log.get('mood', 'N/A')} | "
                            f"Pain: {log.get('pain_level', 'N/A')} | "
                            f"Notes: {log.get('notes', '')}"
                        )
            else:
                st.info("No patient logs available.")

            # --- Staff Logs ---
            st.write("### Staff Logs")
            staff_logs = history.get("staff_logs", {})
            if staff_logs:
                for staff_name, logs in staff_logs.items():
                    with st.expander(f"Logs by {staff_name}", expanded=False):
                        if logs:
                            for log in logs:
                                st.markdown(
                                    f"- **Diagnosis:** {log.get('diagnosis', 'N/A')}  \n"
                                    f"  **Prescription:** {log.get('prescription', 'N/A')}  \n"
                                    f"  **Notes:** {log.get('notes', '')}"
                                )
                        else:
                            st.write("_No logs recorded by this staff member._")
            else:
                st.info("No staff logs available.")
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

def payment_form():
    """Display a form for patients to pay their medical bills."""
    st.header("Pay Medical Bill")

    # Make sure the user is logged in
    if "user" not in st.session_state or st.session_state.user.role.lower() != "patient":
        st.warning("Please log in as a patient to access this feature.")
        return

    user = st.session_state.user
    st.write(f"Logged in as: **{user.user_id}**")

    # Payment form
    with st.form("payment_form"):
        amount = st.number_input("Amount (RM)", min_value=0.0, step=0.5, format="%.2f")
        method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Online Banking", "Cash"])
        notes = st.text_area("Notes (optional)", placeholder="E.g. paying for MRI scan")

        submitted = st.form_submit_button("Submit Payment")
        if submitted:
            if amount <= 0:
                st.error("Please enter a valid payment amount.")
            else:
                patient = patient_bill(user.user_id, amount, method, notes)
                if patient:
                    st.success(f"Payment of RM{amount:.2f} via {method} was successful!")
                else:
                    st.error("Payment failed. Patient record not found.")

def view_billing_history():
    """Display billing/payment history for all patients (admin/staff access)."""
    st.header("View All Patients' Billing History")

    data = load_data(CARELOG_FILE)
    patients = data.get("patients", [])

    if not patients:
        st.warning("No patient records found.")
        return

    has_any_billing = False
    for patient in patients:
        billing_records = patient.get("bills", [])

        if billing_records:
            has_any_billing = True
            with st.expander(f"{patient.get('name', 'Unknown')} (User ID: {patient.get('user_id')})"):
                for i, record in enumerate(billing_records, start=1):
                    st.markdown(f"**Payment {i}:**")
                    st.write(f"- **Amount:** RM {record.get('amount', 'N/A')}")
                    st.write(f"- **Method:** {record.get('method', 'N/A')}")
                    st.write(f"- **Notes:** {record.get('notes', '-')}")
                    st.write(f"- **Timestamp:** {record.get('timestamp', 'N/A')}")
                    st.markdown("---")

    if not has_any_billing:
        st.info("No billing records have been added yet.")

def view_patient_history_admin_page():
    """Display a patient's full history for admins, with dropdown patient selection."""
    user = st.session_state.user
    st.header("View Patient Full History (Admin Access)")

    # Load patient data for dropdown
    data = load_data(CARELOG_FILE)
    patients = data.get("patients", [])

    if not patients:
        st.warning("No patients found in the system.")
        return

    # Build a list of options like "John Doe (P001)"
    patient_options = [f"{p['name']} ({p['user_id']})" for p in patients]
    selected_patient = st.selectbox("Select a Patient", patient_options)

    # Extract patient_id from selection
    patient_id = selected_patient.split("(")[-1].replace(")", "").strip()

    if st.button("View History"):
        status, history = view_patient_history_admin(patient_id)

        if status:
            st.subheader("Patient Details")
            st.write(f"**Ailment:** {history['patient_ailment']}")

            # --- Patient Logs ---
            st.write("### Patient Logs")
            patient_logs = history.get("patient_logs", [])
            if patient_logs:
                for log in patient_logs:
                    timestamp = log.get('timestamp', 'N/A')
                    sensitive = log.get("sensitive_information", False)
                    expander_label = f"{'Sensitive Log - ' if sensitive else ''}{timestamp}"

                    with st.expander(expander_label, expanded=False):
                        if sensitive:
                            st.warning("This log contains sensitive information.")
                        st.markdown(
                            f"- Mood: {log.get('mood', 'N/A')} | "
                            f"Pain: {log.get('pain_level', 'N/A')} | "
                            f"Notes: {log.get('notes', '')}"
                        )
            else:
                st.info("No patient logs available.")

            # --- Staff Logs ---
            st.write("### Staff Logs")
            staff_logs = history.get("staff_logs", {})
            if staff_logs:
                for staff_name, logs in staff_logs.items():
                    with st.expander(f"Logs by {staff_name}", expanded=False):
                        if logs:
                            for log in logs:
                                st.markdown(
                                    f"- **Diagnosis:** {log.get('diagnosis', 'N/A')}  \n"
                                    f"  **Prescription:** {log.get('prescription', 'N/A')}  \n"
                                    f"  **Notes:** {log.get('notes', '')}"
                                )
                        else:
                            st.write("_No logs recorded by this staff member._")
            else:
                st.info("No staff logs available.")
        else:
            st.warning(history)
