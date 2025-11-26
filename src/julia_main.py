# src/julia_main.py
#!/usr/bin/env python3
"""
Julia - File Encryption Tool
Main entry point for PyPI package.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    from julia import main as julia_main
    julia_main()

if __name__ == "__main__":
    main()
