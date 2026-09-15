import hashlib
import os


def hash_password(password):
    salt = os.urandom(16)
    password_hash = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )
    return f"{salt.hex()}:{password_hash.hex()}"


def verify_password(password, stored_hash):
    salt, password_hash = stored_hash.split(':')
    calculated_hash = hashlib.scrypt(
        password.encode(),
        salt=bytes.fromhex(salt),
        n=16384,
        r=8,
        p=1
    )
    return calculated_hash.hex() == password_hash