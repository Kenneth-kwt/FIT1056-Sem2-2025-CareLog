from app.user import User
from utils.storage import load_data, save_data

USER_FILE = "data/careLog.json"

def seed_users():
    """
    Initial users for demo purposes.
    """
    users = [
        {"username": "alice", "password": "123", "role": "patient"},
        {"username": "bob", "password": "123", "role": "staff"},
        {"username": "admin", "password": "admin", "role": "admin"}
    ]
    save_data(USER_FILE, users)

def login(username, password):
    users = load_data(USER_FILE)
    for u in users:
        if u["username"] == username and u["password"] == password:
            return User.from_dict(u)
    return None

def add_user(username, password, role):
    users = load_data(USER_FILE)
    if any(u["username"] == username for u in users):
        return None  # already exists
    user = User(username, password, role)
    users.append(user.to_dict())
    save_data(USER_FILE, users)
    return user