import os
# import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_credentials(text = '', key = '', iv = ''):

    text_bytes = text.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding = pad(text_bytes, 16)
    cipherText = cipher.encrypt(padding)
    print(f'Senha cifrada - {cipherText}')

def decrypt_credentials(cipherText = '', key = ''):
    pass

def initial():
    pass



# iv = os.urandom(16)
# key = os.urandom(16)

# encrypt_credentials('Ac#!e42R', key, iv)