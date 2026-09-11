"""
Funções relacionadas à estrutura de um bloco da blockchain.
"""

import hashlib
import json
from time import time


def new_block(index, transactions, proof, previous_hash=None):
    """
    Cria a estrutura de um novo bloco
    """
    return {
        'index': index,
        'timestamp': time(),
        'transactions': transactions,
        'proof': proof,
        'previous_hash': previous_hash,
    }


def hash(block):
    """
    Gera o hash SHA-256 de um bloco
    :param block: <dict> Bloco que será transformado em hash
    :return: <str> Hash do bloco
    """

    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def valid_block(block):
    """
    Verifica se um bloco possui estrutura e tipos de dados válidos.
    """
    required_fields = ['index', 'timestamp', 'transactions', 'proof', 'previous_hash']

    if not all(field in block for field in required_fields):
        return False

    if not isinstance(block['index'], int):
        return False

    if not isinstance(block['timestamp'], (int, float)):
        return False

    if not isinstance(block['transactions'], list):
        return False

    if not isinstance(block['proof'], int):
        return False

    if not isinstance(block['previous_hash'], (int, str)):
        return False

    return True
