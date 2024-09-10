import argparse
import os
from .file_operations import encrypt_folder, decrypt_folder


def main():
    """
    Handle command-line arguments to perform encryption or decryption
    based on user input, with error handling.
    """

    # Set up command-line argument parsing

    parser = argparse.ArgumentParser(description='Secure File Storage System')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform')
    parser.add_argument('folder', help='Path to the folder to encrypt/decrypt')
    parser.add_argument('password', help='Password for encryption/decryption')

    # Parse the arguments
    args = parser.parse_args()

    try:
        # Check if the folder exists before proceeding
        # Commands should look like: "python -m src.main encrypt "C:\path\to\your\folder" yourpassword"
        # and: "python -m src.main encrypt "C:\path\to\your\folder" yourpassword"
        if not os.path.isdir(args.folder):
            raise FileNotFoundError(f"Folder '{args.folder}' not found. Please provide a valid folder. Command should look like ")

        # Ensure the password is not empty
        if not args.password:
            raise ValueError("Password cannot be empty. Please provide a valid password.")

        # Perform the requested action
        if args.action == 'encrypt':
            encrypt_folder(args.folder, args.password)
            print(f"Folder '{args.folder}' has been encrypted.")
        elif args.action == 'decrypt':
            decrypt_folder(args.folder, args.password)
            print(f"Folder '{args.folder}' has been decrypted.")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except ValueError as val_error:
        print(f"Error: {val_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
