from utils.storage import load_data, save_data
from app.staff import StaffUser
from services.user_service import add_user
from services.user_service import _ensure_structure, delete_user
from app.patient import PatientUser

CARELOG_FILE = "data/careLog.json"

def register_staff(user_id, password, speciality, name):
    """
    Register a new staff member: 
    - Creates a login account (via add_user in user_service)
    - Creates the staff record
    Returns the new StaffUser object if successful, None if user already exists.
    """

    # Step 1: add login account (role = staff)
    user = add_user(user_id, password, role="staff")
    if not user:
        return None  # user already exists

    # Step 2: add staff record
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    new_staff = StaffUser(user_id, password, speciality, name)
    data["staff"].append(new_staff.to_dict())
    data["next_user_id"] = int(user_id) + 1
    # Step 3: save everything
    save_data(CARELOG_FILE, data)

    return new_staff

def add_staff_log(staff_id,patient_id= None,patient_symptoms =None,patient_log_timestamp=None,diagnosis = None,prescription = None,notes = None,patient_logs = None):
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)
    staffs = data.get("staff",[])
    patient = data.get("patients", [])
    found_patient_id = None
    for i,s in enumerate(staffs):
        if s["user_id"] == staff_id:
            #Find the staff 

            for i,p in enumerate(patient):
                if p["user_id"] == patient_id:
                    found_patient_id = p["user_id"]
            if found_patient_id not in s["assigned_patient_ids"]:
                #If patient is not assigned to staff:
                
                print(f'Patient with ID {patient_id} is not assigned to staff of staff ID {staff_id}')
                return None
            else:
                staff = StaffUser.from_dict(s)
                #Create StaffUser object from dic
                # t
                staff.add_log(patient_id= patient_id,patient_symptoms =patient_symptoms,
                              patient_log_timestamp=patient_log_timestamp,
                              diagnosis = diagnosis,
                              prescription = prescription,
                              notes = notes,
                              patient_logs = patient_logs)
                #Create a new log

                data["staff"][i] = staff.to_dict()
                #Store updated staff back into the careLog json file

                save_data(CARELOG_FILE,data)
                return staff
    return None
    #If staff ID isnt found in staff, return none

def find_patient_logs(patient_id,timestamp):
    """Find patients log based on patient ID and timestamp"""
    data = load_data(CARELOG_FILE)
    patients = data.get("patients",[])
    #Load all patients
    for p in patients:
        if p["user_id"] == patient_id:
    #A matching patient is found:

            for l in p["logs"]:
                if p["timestamp"] == timestamp:
    #If corresponding log is found based on timestamp:

                    return l
    #return the corresponding patient log

    return None
    #Not found
            
def view_patient_history(patient_id, staff_id):
    """View patients logs based on patient ID"""
    data = load_data(CARELOG_FILE)
    patients = data.get("patients",[])
    staff = data.get("staff",[])
    staff_logs = {}
    #Dictionary to hold staff logs on patient

    for p in patients:
        if p["user_id"] == patient_id:
            if staff_id not in p["assigned_staff_ids"]:
                #If staff ID isn't assigned to patient, return None
                return False, f'Staff with ID {staff_id} is not assigned to patient with ID {patient_id}'
            patient_logs = p["logs"]
            patient_ailment = p["ailment"]
            for s in staff:
                if s["user_id"] in p["assigned_staff_ids"]:
                    staff_logs[s["name"]] = s["logs"]
    #Store staff logs as "staff_name":[list of logs]
            
            patient_history = {'patient_ailment': patient_ailment,'patient_logs':patient_logs, 'staff_logs':staff_logs}
            return True, patient_history
    #If patient found, return patient ailemnt and logs as 
    return False, f"Patient with ID {patient_id} not found"
    #If patient isn't found, return None
            
