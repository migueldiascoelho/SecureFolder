import os
from .encryption import encrypt_file, decrypt_file
from .key_management import derive_key, generate_salt


def hide_salt_file(salt_file_path: str) -> None:
    """
    Hide the salt file on both Windows and Unix-based systems.
    """
    if os.name == 'nt':  # Windows
        os.system(f'attrib +h "{salt_file_path}"')  # Set hidden attribute on Windows
        print(f"Salt file hidden on Windows: {salt_file_path}")
    else:  # Unix-like (Linux, macOS)
        hidden_salt_file_path = os.path.join(os.path.dirname(salt_file_path), '.' + os.path.basename(salt_file_path))
        os.rename(salt_file_path, hidden_salt_file_path)  # Rename to start with a '.' to hide it on Unix-based systems
        print(f"Salt file hidden on Unix-like OS: {hidden_salt_file_path}")


def encrypt_folder(folder_path: str, password: str) -> None:
    """
    Encrypt all files in the given folder using the provided password.
    """
    # Generate salt and derive a key from the password
    salt = generate_salt()
    key = derive_key(password, salt)

    # Encrypt each file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

    # Save the salt for future decryption
    salt_file_path = os.path.join(folder_path, 'salt.bin')
    with open(salt_file_path, 'wb') as f:
        f.write(salt)

    # Hide the salt file after saving it
    hide_salt_file(salt_file_path)


def decrypt_folder(folder_path: str, password: str) -> None:
    """
    Decrypt all files in the given folder using the provided password, and delete the .enc and salt.bin files.
    """
    # Load the salt
    salt_file_path = os.path.join(folder_path, 'salt.bin')

    # Handle Unix-based hidden salt file (starts with a dot)
    if not os.path.exists(salt_file_path) and not os.path.exists(os.path.join(folder_path, '.salt.bin')):
        print("Salt file not found, cannot decrypt.")
        return

    if not os.path.exists(salt_file_path):
        # If salt.bin is hidden on Unix-like systems
        salt_file_path = os.path.join(folder_path, '.salt.bin')

    with open(salt_file_path, 'rb') as f:
        salt = f.read()

    # Derive the key using the password and salt
    key = derive_key(password, salt)

    # Decrypt each file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                encrypted_file_path = os.path.join(root, file)
                decrypt_file(encrypted_file_path, key)

    # Delete the salt.bin file after decryption
    if os.path.exists(salt_file_path):
        os.remove(salt_file_path)
        print(f"Deleted the salt file: {salt_file_path}")
