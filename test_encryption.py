# test_encryption.py
from src.encryptor import FileEncryptor

def test_encryption():
    """Test basic encryption/decryption functionality"""
    print("Testing File Encryption...")
    
    # Create encryptor instance
    encryptor = FileEncryptor()
    
    # Generate key from password
    password = "my_secure_password_123"
    key, salt = encryptor.generate_key_from_password(password)
    
    # Initialize encryptor with key
    encryptor.initialize_encryptor(key)
    
    # Test string encryption
    test_string = "This is a secret message!"
    encrypted_string = encryptor.encrypt_string(test_string)
    decrypted_string = encryptor.decrypt_string(encrypted_string)
    
    print(f"Original: {test_string}")
    print(f"Encrypted: {encrypted_string}")
    print(f"Decrypted: {decrypted_string}")
    
    # Verify it works
    assert test_string == decrypted_string, "Encryption/Decryption failed!"
    print("String encryption test passed!")
    
    # Test file encryption (create a test file first)
    with open('test_file.txt', 'w') as f:
        f.write("This is test file content for encryption!")
    
    # Encrypt the file
    encrypted_file = encryptor.encrypt_file('test_file.txt')
    
    # Decrypt the file
    decryptor = FileEncryptor()
    decryptor.initialize_encryptor(key)  # Use same key
    decrypted_file = decryptor.decrypt_file(encrypted_file)
    
    # Verify decrypted content
    with open(decrypted_file, 'r') as f:
        content = f.read()
    assert content == "This is test file content for encryption!", "File encryption failed!"
    
    print("File encryption test passed!")
    print("All encryption tests passed!")

if __name__ == "__main__":
    test_encryption()
