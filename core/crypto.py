# Importa a biblioteca responsável pelas operações criptográficas.
from cryptography.hazmat.primitives.asymmetric import ec
# Importa o algoritmo SHA-256 usado para gerar o resumo da mensagem.
from cryptography.hazmat.primitives import hashes

# Gera uma nova chave privada usando a curva secp256k1.
def generate_private_key():
    # Cria e retorna uma chave privada ECDSA aleatória.
    return ec.generate_private_key(ec.SECP256K1())

# Gera a chave pública correspondente a uma chave privada.
def get_public_key(private_key):
    # Obtém e retorna a chave pública derivada da chave privada.
    return private_key.public_key()

# Assina uma mensagem utilizando uma chave privada.
def sign_message(private_key, message):
    # Converte a mensagem para bytes antes da assinatura.
    message = message.encode()
    # Gera e retorna a assinatura digital usando ECDSA e SHA-256.
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Verifica uma assinatura digital utilizando a chave pública.
def verify_signature(public_key, message, signature):
    # Converte a mensagem para bytes antes da verificação.
    message = message.encode()
    # Verifica a assinatura usando ECDSA e SHA-256.
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    # Retorna verdadeiro quando a assinatura é válida.
    return True