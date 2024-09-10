import os
from cryptography.hazmat.backends import default_backend

def generate_salt() -> bytes:
    """
    Generate a cryptographically secure random salt.
    """
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a cryptographic key from the given password and salt.
    """
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    password_bytes = password.encode('utf-8')
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)
    return key

def save_key_to_file(key: bytes, file_path: str) -> None:
    """
    Save the given key to a file.
    """
    with open(file_path, 'wb') as f:
        f.write(key)

def load_key_from_file(file_path: str) -> bytes:
    """
    Load an encryption key from a file.
    """
    with open(file_path, 'rb') as f:
        key = f.read()
    return key
