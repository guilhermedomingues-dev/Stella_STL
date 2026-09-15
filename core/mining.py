"""
Algoritmo de Proof of Work (PoW) da Stella.
"""

import hashlib
from config import MAX_SUPPLY, BLOCK_REWARD, DIFFICULTY, HALVING_INTERVAL


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

def valid_supply(current_supply):
    return current_supply + BLOCK_REWARD <= MAX_SUPPLY

def valid_reward(reward):
    return reward == BLOCK_REWARD

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:DIFFICULTY] == '0' * DIFFICULTY

def get_total_issued(chain):
    total = 0

    for block in chain:
        for transaction in block['transactions']:
            if transaction.get('type') == 'coinbase':
                for output in transaction['outputs']:
                    total += output['amount']

    return total


def valid_coinbase(transaction, chain):
    if transaction.get('type') != 'coinbase':
        return False

    if transaction.get('inputs') != []:
        return False

    outputs = transaction.get('outputs', [])

    if len(outputs) != 1:
        return False

    reward = outputs[0].get('amount')

    if reward != BLOCK_REWARD:
        return False

    return get_total_issued(chain) + reward <= MAX_SUPPLY

def get_block_reward(block_index):
    halvings = (block_index - 1) // HALVING_INTERVAL
    return BLOCK_REWARD // (2 ** halvings)