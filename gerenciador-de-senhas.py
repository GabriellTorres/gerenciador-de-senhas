import os
import base64
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
    padding = pad(text_bytes, AES.block_size)
    cipher_text = cipher.encrypt(padding)

    return iv + cipher_text

def decrypt_credentials(iv_cipher = ''):

    iv = iv_cipher[:AES.block_size]
    cipherText = iv_cipher[AES.block_size:]
    
    key = get_key()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypt_padding = cipher.decrypt(cipherText)

    text_bytes = unpad(decrypt_padding, AES.block_size)

    text = text_bytes.decode('utf-8')

    return text


def preencher_tabela(servico, login, senha):

    arquivo = os.getenv('arq_csv')
    
    with open(arquivo, 'a', encoding='utf-8') as arq:
        arq.seek(0, os.SEEK_END)
        arq.write('\n')
        arq.write(f'{servico},{login},{senha}')
        arq.seek(0, os.SEEK_SET)
        arq.close()

def buscar_senha_tabela(servico, login):

    arquivo = os.getenv('arq_csv')
    senha_retorno = ''
    with open(arquivo, 'r', encoding='utf-8') as arq:
        for numero, linha in enumerate(arq):
            linha = linha.strip()
            if not linha:          
                continue

            partes = linha.split(',')

            if len(partes) == 3:
                servico_arq, login_arq, senha_arq = partes
                if servico_arq.strip() == servico and login_arq.strip() == login:
                    senha_retorno = senha_arq
                    break
            else:
                print(f"Aviso: Linha {numero} inválida ou corrompida ignorada: '{linha}'")
            

        arq.seek(0, os.SEEK_SET)
        arq.close()
    return senha_retorno


def registrar_senha():
    print('Registrando Senha')
    senha64 = ''

    servico = input('Digite o nome do serviço: ').strip().lower()

    login = input('Digite o login do serviço: ').strip()

    senha = input('Digite a senha do serviço:  ').strip()

    iv_senha = os.urandom(AES.block_size)
    chiper_senha = encrypt_credentials(senha, iv_senha)
    senha64 = base64.b64encode(chiper_senha).decode('ascii')

    preencher_tabela(servico, login, senha64)
    return 0


def consultar_senha():
    print('Consultando Senha')

    servico = input('Digite o nome do serviço: ').strip().lower()
    
    login = input('Digite o login do serviço: ').strip()
    
    senha_base64 = buscar_senha_tabela(servico, login)
    print(f'Senha 64: {senha_base64}')
    if not senha_base64:
        raise ValueError(f'Não há senha registrada para {servico} e {login}')

    senha_base64_decode = base64.b64decode(senha_base64)
    senha = decrypt_credentials(senha_base64_decode)
    print(f'Senha referente ao Servico {servico} com login {login}: {senha}')
    

def initial():

    print('=========================================================================')
    print('Selecione o número que representa a funcionalidade que Você deseja: ')
    print('[1] - Registrar uma senha para um serviço: ')
    print('[2] - Consultar senha de um serviço')
    print('=========================================================================')

    servico = input('Qual Serviço deseja: ')

    if servico == "1":
        registrar_senha()

    if servico == "2":
        consultar_senha()
        



initial()

# key = os.urandom(16)


# text_crypt = encrypt_credentials('Ac#!e42R', key, iv)
# decrypt_credentials(text_crypt, key, iv)