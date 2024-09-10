import unittest
import tempfile
import os
from src.file_operations import encrypt_folder, decrypt_folder

class TestFileOperations(unittest.TestCase):

    def test_folder_encryption_and_decryption(self):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a sample file in the temp directory
            sample_file_path = os.path.join(temp_dir, 'test_file.txt')
            with open(sample_file_path, 'w') as f:
                f.write("This is a test file.")

            password = "testpassword"

            # Encrypt the folder
            encrypt_folder(temp_dir, password)

            # Ensure the encrypted file exists
            self.assertTrue(os.path.exists(sample_file_path + ".enc"))

            # Decrypt the folder
            decrypt_folder(temp_dir, password)

            # Ensure the decrypted file matches the original content
            with open(sample_file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, "This is a test file.")

if __name__ == '__main__':
    unittest.main()
