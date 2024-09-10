import unittest
import os
from src.key_management import derive_key, generate_salt, save_key_to_file, load_key_from_file

class TestKeyManagement(unittest.TestCase):

    def setUp(self):
        self.password = "my_password"
        self.salt = generate_salt()
        self.key = derive_key(self.password, self.salt)
        self.key_file_path = 'test_key.bin'

    def tearDown(self):
        # Clean up: remove files
        if os.path.exists(self.key_file_path):
            os.remove(self.key_file_path)

    def test_key_derivation(self):
        # Ensure the key is 32 bytes long (for AES-256)
        self.assertEqual(len(self.key), 32)

    def test_key_storage(self):
        # Save the key to a file
        save_key_to_file(self.key, self.key_file_path)

        # Load the key from the file
        loaded_key = load_key_from_file(self.key_file_path)

        # Ensure the loaded key matches the original key
        self.assertEqual(self.key, loaded_key)

if __name__ == '__main__':
    unittest.main()
