#!/usr/bin/env python3
"""
Julia - File Encryption Tool
Main launcher that provides both CLI and GUI interfaces.
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Julia - File Encryption Tool')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    
    # Parse only the --gui argument, leave the rest for the CLI
    args, unknown_args = parser.parse_known_args()
    
    if args.gui or (len(sys.argv) == 1 and not unknown_args):
        # Launch GUI (only if no other commands provided)
        try:
            from julia_gui import JuliaEncryptionApp
            print("Launching Julia Encryption GUI...")
            app = JuliaEncryptionApp()
            app.run()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to CLI mode...")
            # Pass all arguments to CLI
            sys.argv = [sys.argv[0]] + unknown_args
            from main import main as cli_main
            cli_main()
    else:
        # Use CLI - pass all arguments
        sys.argv = [sys.argv[0]] + unknown_args
        from main import main as cli_main
        cli_main()

if __name__ == "__main__":
    main()
