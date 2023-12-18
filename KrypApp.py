import streamlit as st
import os
from cryptography.fernet import Fernet

# Generate a random key
def generate_key():
    return Fernet.generate_key()

# Encrypt data using a key
def encrypt_data(key, data):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    return encrypted_data

# Decrypt data using a key
def decrypt_data(key, encrypted_data):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data

def main():
    st.title("KrypApp")

    # File upload
    file = st.file_uploader("Choose a file")
    if file is not None:
        file_bytes = file.read()
        filename = os.path.basename(file.name)

    # Secret Key Input (for encryption and decryption)
    secret_key = st.text_input("Enter Secret Key")

    # Encrypt Button
    if st.button('Encrypt'):
        if file_bytes and secret_key:
            # Generate a key
            key = generate_key()

            # Encrypt the file data
            encrypted_data = encrypt_data(key, file_bytes)

            # Save the encrypted file at the imported location
            encrypted_filename = os.path.join(os.path.dirname(os.path.abspath(file.name)), filename + ".encrypted")
            with open(encrypted_filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            st.write(f"File Encrypted and Saved at {encrypted_filename}")
        else:
            st.warning("Please upload a file and enter a key.")

    # Decrypt Button
    if st.button('Decrypt'):
        if file_bytes and secret_key:
            # Decrypt the file data
            decrypted_data = decrypt_data(secret_key.encode(), file_bytes)

            # Save the decrypted file at the imported location
            decrypted_filename = os.path.join(os.path.dirname(os.path.abspath(file.name)), filename.replace(".encrypted", ".decrypted"))
            with open(decrypted_filename, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)

            st.write(f"File Decrypted and Saved at {decrypted_filename}")
        else:
            st.warning("Please upload a file and enter a key.")

if __name__ == "__main__":
    main()
