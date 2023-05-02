# Yamil Ruiz
# Final Project
# Due Date: 03/03/2023

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv
from password_generator import PasswordGenerator

# env key pull from file
load_dotenv()
key = os.environ['FERNETKEY']
"""This should be removed. Left only for educational purpose"""

password = b"password!very1ongkeytouse?562474!"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
keys = base64.urlsafe_b64encode(kdf.derive(password))



# Function to encrypt app password
def password_encrypter(app_pass):
    f = Fernet(key)
    encrypted_pass = f.encrypt(app_pass)
    result = encrypted_pass.decode()
    return result


# Function to decrypt app password
def password_decrypter(app_pass):
    f = Fernet(key)
    decrypted_pass = f.decrypt(app_pass)
    result = decrypted_pass.decode()
    return result


# automatic app password generator
def password_generator():
    pwo = PasswordGenerator()
    pwo.minlen = 10
    result = pwo.generate()
    return result
