import time
from app.user import User

class StaffUser(User):
    def __init__(self, user_id, password,speciality,
                 name,role='staff',assigned_patient_ids = []):
        super().__init__(user_id, password,role)
        self.assigned_patient_ids = assigned_patient_ids
        #This is to be a list to store all assigned patient IDS
        self.speciality = speciality
        self.logs = []
        #To store logs of things
        self.name = name
        #role can be either doctor or nurse

    def to_dict(self):
        staff_dict = {"user_id":self.user_id,
                      "password":self.password,
                      "role":self.role,
                      "name":self.name,
                      "speciality":self.speciality,
                      "assigned_patient_ids":self.assigned_patient_ids,
                      "logs":self.logs
                      }
        return staff_dict
    
    def add_log(self,patient_name= None,
                patient_symptoms =None,patient_log_timestamp=None,
                diagnosis = None,prescription = None,notes = None,
                patient_logs = None):
        #Patient log timestamp is given so that staff can know which patient
        #log to look through if they want additional information on the patient

        #Patient log is an alternative to patient_log_timestamp, such that if the timestamp
        #isn't available but the patient log is, then the timestamp can be found from the patient log
        
        if patient_log_timestamp != None:
            patient_timestamp = patient_log_timestamp
        elif patient_log_timestamp == None and patient_logs != None:
            patient_timestamp = patient_logs["timestamp"]
        else:
            patient_timestamp = None

        log_entry = {
            "patient_name" : patient_name,
            "patient_symptoms" : patient_symptoms,
            "patient_log_timestamp" : patient_timestamp,
            "patient_symptoms" : patient_symptoms,
            "diagnosis" : diagnosis,
            "prescription" : prescription,
            "notes" : notes,
            "staff_log_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return log_entry
    
    @classmethod
    def from_dict(cls, data):
        """Recreate a StaffUser from a JSON dictionary."""
        staff = cls(
            user_id=data.get("user_id"),
            password=data.get("password"),
            role = data.get("role"),
            name = data.get("name"),
            speciality=data.get("speciality"),
            ailment=data.get("ailment"),
            assigned_patient_ids=data.get("assigned_patient_ids",[])

        )
        staff.logs = data.get("logs", [])
        return staff

    

