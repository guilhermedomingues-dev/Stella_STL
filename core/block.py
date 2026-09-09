"""
Funções relacionadas à estrutura de um bloco individual da blockchain.
"""

import hashlib
import json
from operator import index
from time import time

def new_block(self, proof, previous_hash=None):
    """
    Cria um novo bloco e o adiciona à blockchain
    :param proof: <int> Prova encontrada pelo algoritmo de PoW
    :param previous_hash: (Opcional) <str> Hash do bloco anterior
    :return: <dict> Novo bloco criado
    """
    block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'transactions': self.current_transactions,
        'proof': proof,
        'previous_hash': previous_hash or self.hash(self.chain[-1]),
    }

    # Limpa a lista de transações pendentes após incluí-las no novo bloco
    self.current_transactions = []
    self.chain.append(block)
    return block

def hash(block):
    """
    Gera o hash SHA-256 de um bloco
    :param block: <dict> Bloco que será transformado em hash
    :return: <str> Hash do bloco
    """

    # Garante que as chaves do dicionário sejam ordenadas para que o mesmo bloco sempre gere o mesmo hash
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()