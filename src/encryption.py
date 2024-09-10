import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_key(password: bytes, salt: bytes) -> bytes:
    """
    Generate an encryption key using the password and salt.
    """
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key

def encrypt_file(file_path: str, key: bytes) -> None:
    """
    Encrypt the file at the given path using the provided key.
    """
    # Read the file content
    with open(file_path, 'rb') as f:
        data = f.read()

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = iv + encryptor.update(data) + encryptor.finalize()

    # Save the encrypted data to a new file
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)

    # Delete the original file after encryption
    os.remove(file_path)

def decrypt_file(encrypted_file_path: str, key: bytes) -> None:
    """
    Decrypt the encrypted file at the given path using the provided key.
    """
    # Read the encrypted data
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()

    # Extract the IV from the beginning of the file
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

    # Save the decrypted data to a new file (remove '.enc' from the filename)
    original_file_path = encrypted_file_path.replace('.enc', '')
    with open(original_file_path, 'wb') as f:
        f.write(decrypted_data)

    # Delete the .enc file after decryption
    os.remove(encrypted_file_path)
