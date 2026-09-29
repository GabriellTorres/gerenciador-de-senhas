import os
# import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_credentials(text = '', key = '', iv = ''):

    text_bytes = text.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding = pad(text_bytes, 16)
    cipherText = cipher.encrypt(padding)

    return cipherText

def decrypt_credentials(cipherText = '', key = '', iv = ''):

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypt_padding = cipher.decrypt(cipherText)

    text_bytes = unpad(decrypt_padding, 16)

    text = text_bytes.decode('utf-8')

    print(f'texto descriptografado - {text}')


def initial():
    pass



iv = os.urandom(16)
key = os.urandom(16)


text_crypt = encrypt_credentials('Ac#!e42R', key, iv)
decrypt_credentials(text_crypt, key, iv)