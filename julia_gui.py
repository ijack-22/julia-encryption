# julia_gui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from src.encryptor import FileEncryptor
from src.key_manager import KeyManager
from src.file_handler import FileHandler

class JuliaEncryptionApp:
    def __init__(self):
        # Setup appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Julia - File Encryption Tool")
        self.root.geometry("600x500")
        
        # Initialize components
        self.key_manager = KeyManager()
        self.file_handler = FileHandler()
        self.encryptor = FileEncryptor()
        
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Julia File Encryption", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # File selection section
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(file_frame, text="Select File:").pack(anchor="w", padx=10, pady=5)
        
        file_select_frame = ctk.CTkFrame(file_frame)
        file_select_frame.pack(pady=5, padx=10, fill="x")
        
        self.file_path_label = ctk.CTkLabel(file_select_frame, text="No file selected", 
                                           wraplength=400)
        self.file_path_label.pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(file_select_frame, text="Browse", 
                     command=self.select_file).pack(side="right", padx=5)
        
        # Password section
        password_frame = ctk.CTkFrame(main_frame)
        password_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(password_frame, text="Password:").pack(anchor="w", padx=10, pady=5)
        
        self.password_entry = ctk.CTkEntry(password_frame, show="*", placeholder_text="Enter password")
        self.password_entry.pack(pady=5, padx=10, fill="x")
        
        # Key management section
        key_frame = ctk.CTkFrame(main_frame)  # FIXED: Changed main_main_frame to main_frame
        key_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(key_frame, text="Key Name (optional):").pack(anchor="w", padx=10, pady=5)
        
        self.key_entry = ctk.CTkEntry(key_frame, placeholder_text="Enter key name to save")
        self.key_entry.pack(pady=5, padx=10, fill="x")
        
        # Action buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20, padx=10, fill="x")
        
        ctk.CTkButton(button_frame, text="Encrypt File", 
                     command=self.encrypt_file, fg_color="green", hover_color="dark green").pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(button_frame, text="Decrypt File", 
                     command=self.decrypt_file, fg_color="blue", hover_color="dark blue").pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(button_frame, text="Manage Keys", 
                     command=self.manage_keys).pack(side="left", padx=5, fill="x", expand=True)
        
        # Status section
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(status_frame, text="Status:").pack(anchor="w", padx=10, pady=5)
        
        self.status_text = ctk.CTkTextbox(status_frame, height=100)
        self.status_text.pack(pady=5, padx=10, fill="x")
        self.status_text.configure(state="disabled")
    
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Select file to encrypt/decrypt",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.current_file = filename
            self.file_path_label.configure(text=filename)
            self.log_status(f"Selected file: {os.path.basename(filename)}")
    
    def log_status(self, message):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")
        self.root.update()
    
    def encrypt_file(self):
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
        
        try:
            # Generate key from password
            key, salt = self.encryptor.generate_key_from_password(password)
            self.encryptor.initialize_encryptor(key)
            
            # Encrypt file
            output_file = self.current_file + '.encrypted'
            result = self.encryptor.encrypt_file(self.current_file, output_file)
            
            if result:
                self.log_status(f"File encrypted successfully: {os.path.basename(result)}")
                
                # Save key if name provided
                key_name = self.key_entry.get()
                if key_name:
                    self.key_manager.create_key_entry(key_name, key, salt)
                    self.log_status(f"Key saved as: {key_name}")
                
                # Show file hashes
                original_hash = self.file_handler.get_file_hash(self.current_file)
                encrypted_hash = self.file_handler.get_file_hash(result)
                self.log_status(f"Original hash: {original_hash}")
                self.log_status(f"Encrypted hash: {encrypted_hash}")
                
                messagebox.showinfo("Success", "File encrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            self.log_status(f"Error: {str(e)}")
    
    def decrypt_file(self):
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
        
        try:
            key_name = self.key_entry.get()
            if key_name:
                # Use stored key
                key, salt = self.key_manager.get_key(key_name)
                if not key:
                    messagebox.showerror("Error", f"Key '{key_name}' not found.")
                    return
            else:
                # Generate key from password (need salt - limitation for now)
                key, salt = self.encryptor.generate_key_from_password(password)
            
            self.encryptor.initialize_encryptor(key)
            
            # Decrypt file
            result = self.encryptor.decrypt_file(self.current_file)
            
            if result:
                self.log_status(f"File decrypted successfully: {os.path.basename(result)}")
                
                # Show file hash
                decrypted_hash = self.file_handler.get_file_hash(result)
                self.log_status(f"Decrypted hash: {decrypted_hash}")
                
                messagebox.showinfo("Success", "File decrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
            self.log_status(f"Error: {str(e)}")
    
    def manage_keys(self):
        # Create key management window
        key_window = ctk.CTkToplevel(self.root)
        key_window.title("Key Management")
        key_window.geometry("400x300")
        
        # Key list
        ctk.CTkLabel(key_window, text="Stored Keys:", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        keys_frame = ctk.CTkFrame(key_window)
        keys_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        keys = self.key_manager.keys
        if keys:
            for key_name in keys.keys():
                key_frame = ctk.CTkFrame(keys_frame)
                key_frame.pack(pady=2, padx=10, fill="x")
                
                ctk.CTkLabel(key_frame, text=key_name).pack(side="left", padx=5)
                ctk.CTkButton(key_frame, text="Delete", width=60,
                             command=lambda name=key_name: self.delete_key(name, key_window)).pack(side="right", padx=5)
        else:
            ctk.CTkLabel(keys_frame, text="No keys stored").pack(pady=20)
    
    def delete_key(self, key_name, window):
        if self.key_manager.delete_key(key_name):
            self.log_status(f"Key deleted: {key_name}")
            window.destroy()
            self.manage_keys()  # Refresh
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = JuliaEncryptionApp()
    app.run()
