# Encrypt the password and decrypt while retriving 

from cryptography.fernet import Fernet
import base64
import hashlib

def derive_key(password: str, salt: bytes) -> bytes:
    return base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    )

def get_fernet(key: bytes) -> Fernet:
    return Fernet(key)
