import time
from app.user import User

class PatientUser(User):
    """Represents a patient, inheriting from the base User class."""
    def __init__(self, user_id, password, name, age, gender, ailment, culture_and_religion, assigned_staff_ids=None):
        super().__init__(user_id, password, role="patient")
        self.name = name
        self.age = age
        self.gender = gender
        self.ailment = ailment
        self.culture_and_religion = culture_and_religion
        self.logs = []
        self.assigned_staff_ids = assigned_staff_ids or []
        self.bills= []

    def to_dict(self): 
        """Convert PatientUser object into a dictionary for JSON storage."""
        return {
            "user_id": self.user_id,
            "password": self.password,
            "role": self.role,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "ailment": self.ailment,
            "culture_and_religion": self.culture_and_religion,
            "assigned_staff_ids": self.assigned_staff_ids,
            "logs": self.logs,
            "bills": self.bills
        }
    
    def add_log(self, mood=None, pain_level=None, notes=None, sensitive_information=False):
            """Add a new log entry for the patient."""
            if pain_level is not None:
                try:
                    pain_level = int(pain_level)
                    if pain_level < 0 or pain_level > 10:
                        raise ValueError("Pain level must be between 0 and 10")
                except ValueError:
                    pain_level = None
            log_entry = {
                "mood": mood,
                "pain_level": pain_level,
                "notes": notes,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "sensitive_information": bool(sensitive_information)
            }
            self.logs.append(log_entry)

    def pay_bills(self, amount, method, notes=None):
        """
        Pay medical bills as a patient
        """
        bill={
            "amount":amount,
            "method":method,
            "notes":notes or "No notes"
        }
        if bill:
            self.bills.append(bill)
            return True
        return False

    @classmethod
    def from_dict(cls, data):
        """Recreate a PatientUser from a JSON dictionary."""
        patient = cls(
            user_id=data.get("user_id"),
            password=data.get("password"),
            name=data.get("name"),
            age=data.get("age"),
            gender=data.get("gender"),
            ailment=data.get("ailment"),
            culture_and_religion=data.get("culture_and_religion"),
            assigned_staff_ids=data.get("assigned_staff_ids", [])
        )
        patient.logs = data.get("logs", [])
        patient.bills = data.get("bills",[])
        return patient