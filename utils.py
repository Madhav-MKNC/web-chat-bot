# author: Madhav (https://github.com/madhav-mknc)
# utilties / helper functions for app.py


import os
import sys
import hashlib
import json

# Load admin users from the JSON file
USERS_FILE = 'users.json'

USERS = []
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as file:
        USERS = json.load(file)
else:
    print(f"[error] {USERS_FILE} NOT FOUND")
    sys.exit()

# authentication
def is_authenticated(username, password):
    # Check if the provided username and password match any user
    for user in USERS:
        if user['username'] == username and hashlib.sha256(user['password'].encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False

