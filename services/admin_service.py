from utils.storage import load_data, save_data
from app.patient import PatientUser
from services.user_service import add_user
from services.user_service import _ensure_structure, delete_user

CARELOG_FILE = "data/careLog.json"

def assign_staff_to_patient(patient_id, staff_id):
    """
    Assign a staff to a patient by adding the staff's user_id to the patient's assigned_staff_ids list.
    Returns True if successful, False if patient not found or staff already assigned.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    for i, p in enumerate(data["patients"]):
        if p["user_id"] == patient_id:
            patient = PatientUser.from_dict(p)
            if staff_id in patient.assigned_staff_ids:
                return False  # staff already assigned

            patient.assigned_staff_ids.append(staff_id)
            data["patients"][i] = patient.to_dict()
            
            # update staff record as well
            for i, s in enumerate(data["staff"]):
                if s["user_id"] == staff_id:
                    if "assigned_patient_ids" not in s:
                        s["assigned_patient_ids"] = []
                    if patient_id not in s["assigned_patient_ids"]:
                        s["assigned_patient_ids"].append(patient_id)
                    data["staff"][i] = s
                    break
            save_data(CARELOG_FILE, data)
            return True

    return False  # Patient not found

