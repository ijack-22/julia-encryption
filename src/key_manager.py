# src/key_manager.py
import json
import os
import base64
from getpass import getpass

class KeyManager:
    def __init__(self, key_file="encryption_keys.json"):
        self.key_file = key_file
        self.keys = self.load_keys()
    
    def load_keys(self):
        """Load keys from file"""
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading keys: {e}")
                return {}
        return {}
    
    def save_keys(self):
        """Save keys to file"""
        try:
            with open(self.key_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
            print(f"Keys saved to {self.key_file}")
            return True
        except Exception as e:
            print(f"Error saving keys: {e}")
            return False
    
    def create_key_entry(self, key_name, key, salt):
        """Create a new key entry"""
        self.keys[key_name] = {
            'key': base64.b64encode(key).decode(),
            'salt': base64.b64encode(salt).decode()
        }
        return self.save_keys()
    
    def get_key(self, key_name):
        """Retrieve key by name"""
        if key_name in self.keys:
            key_data = self.keys[key_name]
            return (
                base64.b64decode(key_data['key']),
                base64.b64decode(key_data['salt'])
            )
        return None, None
    
    def list_keys(self):
        """List all stored keys"""
        if not self.keys:
            print("No keys stored.")
            return
        
        print("Stored encryption keys:")
        for i, key_name in enumerate(self.keys.keys(), 1):
            print(f"{i}. {key_name}")
    
    def delete_key(self, key_name):
        """Delete a key entry"""
        if key_name in self.keys:
            del self.keys[key_name]
            self.save_keys()
            print(f"Key '{key_name}' deleted.")
            return True
        else:
            print(f"Key '{key_name}' not found.")
            return False
