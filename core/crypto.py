from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


def generate_private_key():
    return ec.generate_private_key(ec.SECP256K1())


def get_public_key(private_key):
    return private_key.public_key()


def sign_message(private_key, message):
    message = message.encode()
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))


def verify_signature(public_key, message, signature):
    message = message.encode()
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    return True