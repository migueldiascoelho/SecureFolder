import unittest
import os
from src.encryption import encrypt_file, decrypt_file, generate_key

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.password = b'my_password'
        self.salt = os.urandom(16)
        self.key = generate_key(self.password, self.salt)
        self.file_path = 'test_file.txt'
        self.encrypted_file_path = self.file_path + '.enc'

        # Create a sample file
        with open(self.file_path, 'w') as f:
            f.write("This is a test.")

    def tearDown(self):
        # Clean up: remove files
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.encrypted_file_path):
            os.remove(self.encrypted_file_path)

    def test_encryption_and_decryption(self):
        # Encrypt the file
        encrypt_file(self.file_path, self.key)

        # Check if the encrypted file is created
        self.assertTrue(os.path.exists(self.encrypted_file_path))

        # Decrypt the file
        decrypt_file(self.encrypted_file_path, self.key)

        # Check if the decrypted file matches the original content
        with open(self.file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "This is a test.")

if __name__ == '__main__':
    unittest.main()
