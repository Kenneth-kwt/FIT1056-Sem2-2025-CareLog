from app.user import User

class AdminUser(User):
    """Represents an admin, inheriting from the base User class."""
    def __init__(self, user_id, password, name):
        super().__init__(user_id, password, role="admin")
        self.name = name

    def to_dict(self): 
        """Convert AdminUser object into a dictionary for JSON storage."""
        return {
            "user_id": self.user_id,
            "password": self.password,
            "role": self.role,
            "name": self.name
        }
    
    def add_user(self, user_id, password, name, role="admin"):
            """Add a new user to the system."""
            new_user = None
            if role == 'admin':
                new_user = AdminUser(user_id, password, name)
            elif role == 'patient':
                new_user = PatientUser(user_id, password, name)
            elif role == 'staff':
                new_user = StaffUser(user_id, password, name)
            return new_user

    @classmethod
    def from_dict(cls, data):
        """Recreate a AdminUser from a JSON dictionary."""
        admin = cls(
            user_id=data.get("user_id"),
            password=data.get("password"),
            name=data.get("name")
        )
        return admin