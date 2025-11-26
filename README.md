# Julia - File Encryption Tool

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A secure, user-friendly file encryption tool with both GUI and CLI interfaces using AES-256 encryption.

## Features

- **Modern GUI**: Easy-to-use graphical interface with dark theme
- **CLI Support**: Command-line interface for automation and scripting
- **AES-256 Encryption**: Military-grade encryption algorithm
- **Password-Based Keys**: Secure key derivation using PBKDF2
- **Key Management**: Store and manage multiple encryption keys
- **File Integrity**: SHA-256 hash verification
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

```bash
git clone https://github.com/ijack-22/julia-encryption.git
cd julia-encryption
python3 -m venv julia-env
source julia-env/bin/activate
pip install -r requirements.txt
Usage
GUI Mode (Recommended)
bash

python julia.py
# or
python julia.py --gui

CLI Mode
bash

# Encrypt a file
python julia.py encrypt document.pdf --key-name "my_key"

# Decrypt a file  
python julia.py decrypt document.pdf.encrypted --key-name "my_key"

# Manage keys
python julia.py keys list
python julia.py keys create --name "new_key"

Project Structure
julia-encryption/
├── src/
│   ├── encryptor.py      # Core encryption/decryption
│   ├── key_manager.py    # Key storage and management
│   ├── file_handler.py   # File operations
│   └── __init__.py
├── julia_gui.py         # Graphical interface
├── julia.py            # Main launcher
├── main.py             # CLI interface
├── requirements.txt    # Dependencies
└── README.md
Security

    AES-256 symmetric encryption

    PBKDF2 key derivation with 100,000 iterations

    Random salt generation

    Secure key storage

    SHA-256 file integrity checks

Requirements

    Python 3.7+

    cryptography

    customtkinter
