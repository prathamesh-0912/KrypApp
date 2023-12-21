#!/usr/bin/env python3
"""
    Name: KrypApp
    Type: File Encryption GUI App
"""
import streamlit as st
import os
from Crypto.Cipher import AES
import hashlib
import os
import sys
# import threading


class EncryptionTool:
    """ "EncryptionTool" class from "github.com/nsk89" for file encryption.
    (Has been modified a bit.) """
    def __init__(self, user_file, user_key, user_salt):
        # get the path to input file
        self.user_file = user_file

        self.input_file_size = os.path.getsize(self.user_file)
        self.chunk_size = 1024
        self.total_chunks = (self.input_file_size // self.chunk_size) + 1
        
        # convert the key and salt to bytes
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")

        # get the file extension
        self.file_extension = self.user_file.split(".")[-1]
        
        # hash type for hashing key and salt
        self.hash_type = "SHA256"

        # encrypted file name
        self.encrypt_output_file = ".".join(self.user_file.split(".")[:-1]) \
            + "." + self.file_extension + ".kryp"

        # decrypted file name
        self.decrypt_output_file = self.user_file[:-5].split(".")
        self.decrypt_output_file = ".".join(self.decrypt_output_file[:-1]) \
            + "__dekrypted__." + self.decrypt_output_file[-1]

        # dictionary to store hashed key and salt
        self.hashed_key_salt = dict()

        # hash key and salt into 16 bit hashes
        self.hash_key_salt()

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        Code Courtesy: https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def encrypt(self):
        # create a cipher object
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )

        self.abort() # if the output file already exists, remove it first

        input_file = open(self.user_file, "rb")
        output_file = open(self.encrypt_output_file, "ab")
        done_chunks = 0

        for piece in self.read_in_chunks(input_file, self.chunk_size):
            encrypted_content = cipher_object.encrypt(piece)
            output_file.write(encrypted_content)
            done_chunks += 1
            yield (done_chunks / self.total_chunks) * 100
        
        input_file.close()
        output_file.close()

        # Save the hashed key to a file
        key_file = self.encrypt_output_file + ".key"
        with open(key_file, "w") as file:
            file.write(self.hashed_key_salt["key"].decode())

    def decrypt(self):
        
        # Read and verify the hashed key
        key_file = self.user_file + ".key"
        if not os.path.isfile(key_file):
            raise Exception("Key file not found. Cannot verify the key.")
        
        with open(key_file, "r") as file:
            saved_key = file.read()
        if saved_key != self.hashed_key_salt["key"].decode():
            raise Exception("Incorrect key provided for decryption.")
        #  exact same as above function except in reverse
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )

        self.abort() # if the output file already exists, remove it first

        input_file = open(self.user_file, "rb")
        output_file = open(self.decrypt_output_file, "xb")
        done_chunks = 0

        for piece in self.read_in_chunks(input_file):
            decrypted_content = cipher_object.decrypt(piece)
            output_file.write(decrypted_content)
            done_chunks += 1
            yield (done_chunks / self.total_chunks) * 100
        
        input_file.close()
        output_file.close()

        # clean up the cipher object
        del cipher_object

    def abort(self):
        if os.path.isfile(self.encrypt_output_file):
            os.remove(self.encrypt_output_file)
        if os.path.isfile(self.decrypt_output_file):
            os.remove(self.decrypt_output_file)


    def hash_key_salt(self):
        # --- convert key to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)

        # turn the output key hash into 32 bytes (256 bits)
        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")

        # clean up hash object
        del hasher

        # --- convert salt to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)

        # turn the output salt hash into 16 bytes (128 bits)
        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")
        
        # clean up hash object
        del hasher

st.title('KrypApp - File Encryption App')

# File Upload
uploaded_file = st.file_uploader("Choose a file to encrypt/decrypt", type=None)
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name

# User Inputs for Key and Operation
secret_key = st.text_input("Enter your Secret Key", type="password")
operation = st.radio("Choose Operation", ('Encrypt', 'Decrypt'))

# Encrypt/Decrypt Logic
def process_file(operation, secret_key, file_bytes, filename):
    # Convert key and salt
    user_key = bytes(secret_key, "utf-8")
    user_salt = bytes(secret_key[::-1], "utf-8")

    # Hash key and salt
    hasher = hashlib.sha256()
    hasher.update(user_key)
    hashed_key = hasher.digest()[:32]

    hasher = hashlib.sha256()
    hasher.update(user_salt)
    hashed_salt = hasher.digest()[:16]

    # Create cipher object
    cipher = AES.new(hashed_key, AES.MODE_CFB, hashed_salt)

    # Encrypt/Decrypt
    if operation == 'Encrypt':
        processed_bytes = cipher.encrypt(file_bytes)
        output_filename = "encrypted_" + filename
    else:
        processed_bytes = cipher.decrypt(file_bytes)
        output_filename = "decrypted_" + filename

    return processed_bytes, output_filename

# Process File
if st.button(f'{operation} File') and uploaded_file is not None:
    processed_bytes, output_filename = process_file(operation, secret_key, file_bytes, filename)

    # Download Link
    st.download_button(
        label="Download File",
        data=processed_bytes,
        file_name=output_filename,
        mime='application/octet-stream'
    )

