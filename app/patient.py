from app.user import User

class PatientUser(User):
    """Represents a patient, inheriting from the base User class."""
    def __init__(self, user_id, name, ailment, assigned_doctor_ids=None):
        super().__init__(user_id, name)
        self.ailment = ailment
        self.assigned_doctor_ids = assigned_doctor_ids or []

    def to_dict(self): 
        """A method that turns a studentUser object to a plain dictionary to be used."""
        return {
            "id": self.id,
            "name": self.name,
            "ailment": self.ailment,
            "assigned_doctor_ids": self.assigned_doctor_ids
        }
    
    @classmethod
    def from_dict(cls, data):
        """Build a PatientUser from JSON dict."""
        return cls(
            user_id=data.get("id"),
            name=data.get("name"),
            ailment=data.get("ailment"),
            assigned_doctor_ids=data.get("assigned_doctor_ids", [])
        )