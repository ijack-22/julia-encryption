import unittest
import os
import tempfile
from src.key_manager import KeyManager

class TestKeyManager(unittest.TestCase):
    
    def setUp(self):
        self.temp_key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json').name
        self.key_manager = KeyManager(self.temp_key_file)
    
    def tearDown(self):
        if os.path.exists(self.temp_key_file):
            os.unlink(self.temp_key_file)
    
    def test_create_and_retrieve_key(self):
        test_key = b"test_key_123456789012345678901234567890"
        test_salt = b"test_salt_123456"
        
        result = self.key_manager.create_key_entry("test_key", test_key, test_salt)
        self.assertTrue(result)
        
        retrieved_key, retrieved_salt = self.key_manager.get_key("test_key")
        self.assertEqual(retrieved_key, test_key)

if __name__ == '__main__':
    unittest.main()
