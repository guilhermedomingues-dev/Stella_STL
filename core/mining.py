"""
Algoritmo de Proof of Work (PoW) da Stella.
"""

import hashlib


def proof_of_work(last_proof):
    """
    Procura uma prova cujo hash da prova anterior com a nova prova
    comece com quatro zeros.
    """
    proof = 0

    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


def valid_proof(last_proof, proof):
    """
    Verifica se a prova atende à dificuldade definida pelo protocolo.
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:4] == "0000"