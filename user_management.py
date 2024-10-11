import os
import hashlib
from cryptography.fernet import Fernet

# Function to generate encryption key and store it securely
def generate_key():
    key = Fernet.generate_key()
    with open("user_secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load encryption key
def load_key():
    return open("user_secret.key", "rb").read()

# Function to save user credentials
def save_credentials(username, password):
    key = load_key()
    fernet = Fernet(key)

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Prepare credentials to encrypt
    credentials = f"{username}:{hashed_password}\n".encode()

    # Encrypt and save the credentials
    encrypted_data = fernet.encrypt(credentials)
    with open("user_credentials.enc", "ab") as cred_file:
        cred_file.write(encrypted_data)

# Function to load and verify user credentials
def verify_user(username, password):
    key = load_key()
    fernet = Fernet(key)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open("user_credentials.enc", "rb") as cred_file:
            for line in cred_file:
                decrypted_line = fernet.decrypt(line).decode()
                stored_username, stored_password = decrypted_line.split(":")
                if stored_username == username and stored_password == hashed_password:
                    return True
    except FileNotFoundError:
        print("No user credentials found.")
    return False

# Function to register a new user
def register_user(username, password):
    save_credentials(username, password)
    print(f"User '{username}' registered successfully.")

# Create a key for encryption (run once)
if not os.path.exists("user_secret.key"):
    generate_key()
