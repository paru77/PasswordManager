# Master password authentication if exist or create a new one

import os
import hashlib
import json
import getpass

AUTH_FILE = 'auth.json'

def hash_password(password: str) -> str:
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def setup_master_password():
    print("No master password found. Set up a new one.")
    password = getpass.getpass("New Master Password: ")
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("Passwords do not match!")
        return False

    salt = os.urandom(16)
    hashed = hash_password(password)

    with open(AUTH_FILE, 'w') as f:
        json.dump({"hash": hashed, "salt": salt.hex()}, f)

    print("Master password set.")
    return True

def verify_master_password():
    if not os.path.exists(AUTH_FILE):
        setup_master_password()
    

    with open(AUTH_FILE, 'r') as f:
        data = json.load(f)

    salt = bytes.fromhex(data['salt'])
    correct_hash = data['hash']

    password = getpass.getpass("Enter Master Password for Verification: ")
    if hash_password(password) == correct_hash:
        print("Master password verified.")
        return password, salt
    else:
        print("Incorrect password.")
        return None, None
