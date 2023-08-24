import tkinter as tk
from tkinter import filedialog, messagebox

class EncryptionTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Encryption Tool")

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        self.file_path = tk.StringVar()
        self.encryption_key = tk.StringVar()
        self.encrypted_text = tk.StringVar()

        self.file_label = tk.Label(self.root, text="File Path:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.root, textvariable=self.file_path)
        self.file_entry.pack()

        self.key_label = tk.Label(self.root, text="Encryption Key:")
        self.key_label.pack()

        self.key_entry = tk.Entry(self.root, textvariable=self.encryption_key)
        self.key_entry.pack()

        self.encrypt_button = tk.Button(self.root, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack()

        self.encrypted_text_label = tk.Label(self.root, text="Encrypted Text:")
        self.encrypted_text_label.pack()

        self.encrypted_text_label = tk.Label(self.root, textvariable=self.encrypted_text)
        self.encrypted_text_label.pack()

    def encrypt(self):
        try:
            file_path = self.file_path.get()
            encryption_key = self.encryption_key.get()

            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            encrypted_content = self.simple_encrypt(file_content, encryption_key)
            self.encrypted_text.set(encrypted_content)
        except Exception as e
            messagebox.showerror("Error", str(e))

    def simple_encrypt(self, data, key):
        key_bytes = key.encode('utf-8')
        encrypted_data = bytearray()

        for i, byte in enumerate(data):
            encrypted_byte = byte ^ key_bytes[i % len(key_bytes)]
            encrypted_data.append(encrypted_byte)

        return encrypted_data.hex()

if __name__ == "__main__":
    EncryptionTool()
