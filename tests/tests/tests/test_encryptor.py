import unittest
import os
import tempfile
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.encryptor import FileEncryptor

class TestFileEncryptor(unittest.TestCase):
    
    def setUp(self):
        self.encryptor = FileEncryptor()
        self.test_password = "test_password_123"
        self.key, self.salt = self.encryptor.generate_key_from_password(self.test_password)
        self.encryptor.initialize_encryptor(self.key)
    
    def test_key_generation(self):
        key, salt = self.encryptor.generate_key_from_password("test")
        self.assertIsNotNone(key)
        self.assertIsNotNone(salt)
        self.assertEqual(len(salt), 16)
    
    def test_string_encryption_decryption(self):
        original_text = "This is a secret message!"
        encrypted = self.encryptor.encrypt_string(original_text)
        decrypted = self.encryptor.decrypt_string(encrypted)
        self.assertEqual(original_text, decrypted)

if __name__ == '__main__':
    unittest.main()
