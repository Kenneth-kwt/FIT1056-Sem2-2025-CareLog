from utils.storage import load_data, save_data
from app.patient import PatientUser
from services.user_service import add_user
from services.user_service import _ensure_structure, delete_user

CARELOG_FILE = "data/careLog.json"

def add_patient_log(user_id, mood=None, pain_level=None, notes=None, sensitive_information=False):
    """
    Add a new mood/pain log for a specific patient and save it to careLog.json.
    Uses the add_log() method from PatientUser.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)
    patients = data.get("patients", [])
    for i, p in enumerate(patients):
        if p["user_id"] == user_id:
            # Recreate PatientUser object from dict
            patient = PatientUser.from_dict(p)

            # Use the existing method in patient.py
            patient.add_log(mood=mood, pain_level=pain_level, notes=notes, sensitive_information=sensitive_information)

            # Replace the old record with updated one
            data["patients"][i] = patient.to_dict()

            # Save back to file
            save_data(CARELOG_FILE, data)
            return patient  # Return the updated patient object

    return None  # Patient not found

def register_patient(user_id, password, name, age, gender, ailment, culture_and_religion):
    """
    Register a new patient: 
    - Creates a login account (via add_user in user_service)
    - Creates the patient record
    Returns the new PatientUser object if successful, None if user already exists.
    """

    # Step 1: add login account (role = patient)
    user = add_user(user_id, password, role="patient")
    if not user:
        return None  # user already exists

    # Step 2: add patient record
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    new_patient = PatientUser(user_id, password, name, age, gender, ailment, culture_and_religion)
    data["patients"].append(new_patient.to_dict())
    data["next_user_id"] = int(user_id) + 1
    # Step 3: save everything
    save_data(CARELOG_FILE, data)

    return new_patient

def delete_patient(user_id):
    """
    Delete a patient and their corresponding user account from careLog.json.
    Returns True if deleted, False if not found.
    """
    # Step 1: delete the login account using existing function
    user_deleted = delete_user(user_id)

    # Step 2: remove patient record
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    patients_before = len(data["patients"])
    data["patients"] = [p for p in data["patients"] if p["user_id"] != user_id]

    patient_deleted = len(data["patients"]) != patients_before

    # If either user or patient was deleted, save changes
    if user_deleted or patient_deleted:
        save_data(CARELOG_FILE, data)
        return True

    return False

def patient_bill(user_id,amount,method,notes=None):
    """
    Pay medical bills as a patient
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)
    patients = data.get("patients", [])
    for i, p in enumerate(patients):
        if p["user_id"] == user_id:
            patient = PatientUser.from_dict(p)
            patient.pay_bills(amount,method,notes)
            data["patients"][i] = patient.to_dict()
            save_data(CARELOG_FILE, data)
            return patient
    return None