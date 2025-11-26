import unittest
import os
import tempfile
from src.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    
    def setUp(self):
        self.file_handler = FileHandler()
    
    def test_file_exists(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            self.assertTrue(self.file_handler.file_exists(temp_file))
            self.assertFalse(self.file_handler.file_exists("/nonexistent/path/file.txt"))
        finally:
            os.unlink(temp_file)

if __name__ == '__main__':
    unittest.main()
