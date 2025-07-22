import os
import json

USER_DATA_FILE = "users.json"

# Create file if it doesn't exist
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def add_user(username, password):
    users = load_users()
    if username in users:
        return False  # already exists
    users[username] = password
    save_users(users)
    return True

def validate_user(username, password):
    users = load_users()
    return users.get(username) == password
