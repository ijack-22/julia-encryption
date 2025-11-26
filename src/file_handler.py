# src/file_handler.py
import os
import hashlib

class FileHandler:
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path)
    
    @staticmethod
    def get_file_hash(file_path):
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error calculating file hash: {e}")
            return None
    
    @staticmethod
    def validate_file_size(file_path, max_size_mb=100):
        """Check if file size is within limits"""
        try:
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            
            if size_mb > max_size_mb:
                print(f"Warning: File size {size_mb:.2f}MB exceeds {max_size_mb}MB limit")
                return False
            return True
        except Exception as e:
            print(f"Error checking file size: {e}")
            return False
    
    @staticmethod
    def get_file_info(file_path):
        """Get file information"""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
