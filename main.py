# main.py
import argparse
import os
from src.encryptor import FileEncryptor
from src.key_manager import KeyManager
from src.file_handler import FileHandler
from getpass import getpass

def main():
    parser = argparse.ArgumentParser(description='File Encryption Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('file', help='File to encrypt')
    encrypt_parser.add_argument('-o', '--output', help='Output file name')
    encrypt_parser.add_argument('-k', '--key-name', help='Key name for storage')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('file', help='File to decrypt')
    decrypt_parser.add_argument('-o', '--output', help='Output file name')
    decrypt_parser.add_argument('-k', '--key-name', help='Key name to use')
    
    # Key management commands
    key_parser = subparsers.add_parser('keys', help='Key management')
    key_parser.add_argument('action', choices=['list', 'create', 'delete'], 
                          help='Key action to perform')
    key_parser.add_argument('--name', help='Key name for create/delete')
    
    args = parser.parse_args()
    
    key_manager = KeyManager()
    file_handler = FileHandler()
    
    if args.command == 'encrypt':
        encrypt_file(args.file, args.output, args.key_name, key_manager, file_handler)
    
    elif args.command == 'decrypt':
        decrypt_file(args.file, args.output, args.key_name, key_manager, file_handler)
    
    elif args.command == 'keys':
        manage_keys(args.action, args.name, key_manager)
    
    else:
        parser.print_help()

def encrypt_file(input_file, output_file, key_name, key_manager, file_handler):
    """Encrypt a file"""
    if not file_handler.file_exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return
    
    if not file_handler.validate_file_size(input_file):
        return
    
    password = getpass("Enter encryption password: ")
    if not password:
        print("Error: Password cannot be empty.")
        return
    
    encryptor = FileEncryptor()
    key, salt = encryptor.generate_key_from_password(password)
    encryptor.initialize_encryptor(key)
    
    result = encryptor.encrypt_file(input_file, output_file)
    
    if result and key_name:
        key_manager.create_key_entry(key_name, key, salt)
        print(f"Key saved as '{key_name}'")
    
    if result:
        original_hash = file_handler.get_file_hash(input_file)
        encrypted_hash = file_handler.get_file_hash(result)
        print(f"Original file hash: {original_hash}")
        print(f"Encrypted file hash: {encrypted_hash}")

def decrypt_file(input_file, output_file, key_name, key_manager, file_handler):
    """Decrypt a file"""
    if not file_handler.file_exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return
    
    encryptor = FileEncryptor()
    
    if key_name:
        # Use stored key
        key, salt = key_manager.get_key(key_name)
        if key:
            encryptor.initialize_encryptor(key)
        else:
            print(f"Error: Key '{key_name}' not found.")
            return
    else:
        # Use password
        password = getpass("Enter decryption password: ")
        if not password:
            print("Error: Password cannot be empty.")
            return
        
        # For decryption, we need the salt - this is a limitation we'll fix later
        print("Note: Salt required for decryption. Using stored keys is recommended.")
        salt = input("Enter salt (base64) or leave empty to skip: ")
        if salt:
            salt = base64.b64decode(salt)
        else:
            salt = None
        
        key, _ = encryptor.generate_key_from_password(password, salt)
        encryptor.initialize_encryptor(key)
    
    result = encryptor.decrypt_file(input_file, output_file)
    
    if result:
        decrypted_hash = file_handler.get_file_hash(result)
        print(f"Decrypted file hash: {decrypted_hash}")

def manage_keys(action, key_name, key_manager):
    """Manage encryption keys"""
    if action == 'list':
        key_manager.list_keys()
    
    elif action == 'create':
        if not key_name:
            print("Error: Key name required for creation.")
            return
        
        password = getpass("Enter password for key generation: ")
        if not password:
            print("Error: Password cannot be empty.")
            return
        
        encryptor = FileEncryptor()
        key, salt = encryptor.generate_key_from_password(password)
        
        if key_manager.create_key_entry(key_name, key, salt):
            print(f"Key '{key_name}' created successfully.")
    
    elif action == 'delete':
        if not key_name:
            print("Error: Key name required for deletion.")
            return
        key_manager.delete_key(key_name)

if __name__ == "__main__":
    main()
