from app.user import User
from utils.storage import load_data, save_data

CARELOG_FILE = "data/careLog.json"

def _ensure_structure(data):
    """
    Ensure the JSON always has the structure:
    {
        "users": [],
        "patients": [],
        "staff":[]
    }
    """
    if not data or not isinstance(data, dict):
        return {"users": [], "patients": [],"staff":[]}
    if "users" not in data:
        data["users"] = []
    if "patients" not in data:
        data["patients"] = []
    if "staff" not in data:
        data["staff"] = []
    return data

def seed_users():
    """
    Seed initial users into careLog.json with default structure.
    Only runs if the file has no users yet.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    if not data["users"]:  # only seed if no users exist
        data["users"] = [
            {"user_id": "alice", "password": "123", "role": "patient"},
            {"user_id": "bob", "password": "123", "role": "staff"},
            {"user_id": "admin", "password": "admin", "role": "admin"}
        ]
        save_data(CARELOG_FILE, data)

def login(user_id, password):
    """
    Attempt to log in a user by checking user_id + password.
    Returns a User object if successful, otherwise None.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)
    for u in data["users"]:
        if u["user_id"] == user_id and u["password"] == password:
            return User.from_dict(u)
    return None

def add_user(user_id, password, role):
    """
    Add a new user to the careLog.json file.
    Returns the new User object if successful, None if user already exists.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    if any(u["user_id"] == user_id for u in data["users"]):
        return None  # already exists

    user = User(user_id, password, role)
    data["users"].append(user.to_dict())
    save_data(CARELOG_FILE, data)
    return user

def delete_user(user_id: str) -> bool:
    """
    Delete a user from careLog.json.
    Returns True if deleted, False if not found.
    """
    data = load_data(CARELOG_FILE)
    data = _ensure_structure(data)

    # Remove user from users
    users_before = len(data["users"])
    data["users"] = [u for u in data["users"] if u["user_id"] != user_id]

    if len(data["users"]) == users_before:
        return False  # nothing deleted

    save_data(CARELOG_FILE, data)
    return True
