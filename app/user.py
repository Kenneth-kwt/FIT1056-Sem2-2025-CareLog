class User:
    def __init__(self, user_id, password, role):
        """
        role: "patient", "staff", "admin"
        """
        self.user_id = user_id
        self.password = password  # plaintext for MVP (not secure in real systems!)
        self.role = role

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "password": self.password,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return User(data["user_id"], data["password"], data["role"])