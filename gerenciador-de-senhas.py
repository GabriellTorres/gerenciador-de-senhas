import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv

load_dotenv()

def get_key():
    key_hex = os.getenv("KEY")
    if key_hex is None:
        raise ValueError('Variável key não encontrada no .env')
    return bytes.fromhex(key_hex)

def encrypt_credentials(text = '', iv = ''):

    key = get_key()

    text_bytes = text.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding = pad(text_bytes, 16)
    cipherText = cipher.encrypt(padding)

    return cipherText

def decrypt_credentials(cipherText = '', iv = ''):

    key = get_key()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypt_padding = cipher.decrypt(cipherText)

    text_bytes = unpad(decrypt_padding, 16)

    text = text_bytes.decode('utf-8')

    print(f'texto descriptografado - {text}')


def registrarSenha():
    print('Registrando Senha')
    iv = os.urandom(16)

    servico = input('Digite o nome do serviço: ')

    senha_login = input('Deseja criptografar Login e Senha? (Y/N)')
    senha_login.lower()

    bool_senha_login = False
    if senha_login == 'y':
        bool_senha_login = True


    login = input('Digite o login do serviço: ')
    senha = input('Digite a senha do serviço:  ')

    cipher = encrypt_credentials(senha, iv)
    decrypt_credentials(cipher, iv)



    # servico = input('Digite o serviço que seja registrar: ')
    # login = input('Digite o login do serviço: ')
    # senha = input('Digite a senha do serviço:  ')

def initial():

    print('=========================================================================')
    print('Selecione o número que representa a funcionalidade que Você deseja: ')
    print('[1] - Registrar uma senha para um serviço: ')
    print('=========================================================================')

    servico = input('Qual Serviço deseja: ')

    if servico == "1":
        registrarSenha()



initial()

# key = os.urandom(16)


# text_crypt = encrypt_credentials('Ac#!e42R', key, iv)
# decrypt_credentials(text_crypt, key, iv)