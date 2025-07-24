# Entry point for the code

import json
import os
from crypto_utils import derive_key, get_fernet
from auth import verify_master_password
import getpass

VAULT_FILE = 'vault.json'

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, 'r') as f:
        return json.load(f)

def save_vault(vault):
    with open(VAULT_FILE, 'w') as f:
        json.dump(vault, f)

def add_credential(fernet):
    site = input("Website: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    encrypted_password = fernet.encrypt(password.encode()).decode()
    vault = load_vault()
    vault[site] = {
        "username": username,
        "password": encrypted_password
    }
    save_vault(vault)
    print("Credential saved.")

def retrieve_credential(fernet):
    site = input("Website to retrieve: ")
    vault = load_vault()

    if site not in vault:
        print("No credentials found for that site.")
        return

    entry = vault[site]
    decrypted_password = fernet.decrypt(entry["password"].encode()).decode()

    print(f"Username: {entry['username']}")
    print(f"Password: {decrypted_password}")

def main():
    password, salt = verify_master_password()
    if not password:
        return

    key = derive_key(password, salt)
    fernet = get_fernet(key)

    while True:
        print("\nChoose an option:")
        print("1. Add Credential")
        print("2. Retrieve Credential")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            add_credential(fernet)
        elif choice == '2':
            retrieve_credential(fernet)
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
