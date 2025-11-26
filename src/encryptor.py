# src/encryptor.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class FileEncryptor:
    def __init__(self):
        self.fernet = None
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def initialize_encryptor(self, key: bytes):
        """Initialize Fernet encryptor with key"""
        self.fernet = Fernet(key)
    
    def encrypt_file(self, input_file: str, output_file: str = None) -> str:
        """Encrypt a file"""
        if not self.fernet:
            raise ValueError("Encryptor not initialized. Call initialize_encryptor() first.")
        
        if output_file is None:
            output_file = input_file + '.encrypted'
        
        try:
            # Read file content
            with open(input_file, 'rb') as file:
                file_data = file.read()
            
            # Encrypt data
            encrypted_data = self.fernet.encrypt(file_data)
            
            # Write encrypted file
            with open(output_file, 'wb') as file:
                file.write(encrypted_data)
            
            print(f"File encrypted successfully: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Encryption failed: {e}")
            return None
    
    def decrypt_file(self, input_file: str, output_file: str = None) -> str:
        """Decrypt a file"""
        if not self.fernet:
            raise ValueError("Encryptor not initialized. Call initialize_encryptor() first.")
        
        if output_file is None:
            if input_file.endswith('.encrypted'):
                output_file = input_file.replace('.encrypted', '.decrypted')
            else:
                output_file = input_file + '.decrypted'
        
        try:
            # Read encrypted file
            with open(input_file, 'rb') as file:
                encrypted_data = file.read()
            
            # Decrypt data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Write decrypted file
            with open(output_file, 'wb') as file:
                file.write(decrypted_data)
            
            print(f"File decrypted successfully: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

    def encrypt_string(self, text: str) -> str:
        """Encrypt a string"""
        if not self.fernet:
            raise ValueError("Encryptor not initialized.")
        return self.fernet.encrypt(text.encode()).decode()
    
    def decrypt_string(self, encrypted_text: str) -> str:
        """Decrypt a string"""
        if not self.fernet:
            raise ValueError("Encryptor not initialized.")
        return self.fernet.decrypt(encrypted_text.encode()).decode()
