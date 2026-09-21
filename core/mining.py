"""
Algoritmo de Proof of Work (PoW) da Stella.
"""

import hashlib
from config import MAX_SUPPLY, BLOCK_REWARD, DIFFICULTY, HALVING_INTERVAL, TARGET_BLOCK_TIME, MAX_HALVINGS

def get_difficulty(chain):
    if len(chain) < 2:
        return DIFFICULTY

    last_block = chain[-1]
    previous_block = chain[-2]

    actual_time = last_block['timestamp'] - previous_block['timestamp']

    if actual_time <= 0:
        return DIFFICULTY

    difficulty = DIFFICULTY * TARGET_BLOCK_TIME / actual_time

    return max(1, round(difficulty))

def proof_of_work(last_proof):
    """
    Procura uma prova cujo hash da prova anterior com a nova prova
    comece com quatro zeros.
    """
    proof = 0

    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

def valid_supply(current_supply):
    return current_supply + BLOCK_REWARD <= MAX_SUPPLY

def valid_reward(reward):
    return reward == BLOCK_REWARD

def valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == '0' * difficulty

def get_total_issued(chain):
    total = 0

    for block in chain:
        for transaction in block['transactions']:
            if transaction.get('type') == 'coinbase':
                for output in transaction['outputs']:
                    total += output['amount']

    return total


def valid_coinbase(transaction, chain, block_index, block_transactions=None):
    if transaction.get('type') != 'coinbase':
        return False

    if transaction.get('inputs') != []:
        return False

    if transaction.get('block_index') != block_index:
        return False

    outputs = transaction.get('outputs', [])

    if len(outputs) != 1:
        return False

    reward = outputs[0].get('amount')
    expected_reward = get_block_reward(block_index)

    total_fees = 0

    if block_transactions:
        for tx in block_transactions:
            if tx.get('type') == 'coinbase':
                continue

            total_fees += tx.get('fee', 0)

    expected_total = expected_reward + total_fees

    if reward != expected_total:
        return False

    return get_total_issued(chain) + expected_reward <= MAX_SUPPLY

def get_halving_count(block_index):
    return (block_index - 1) // HALVING_INTERVAL

def get_block_reward(block_index):
    halvings = get_halving_count(block_index)

    if halvings >= MAX_HALVINGS:
        return 0

    reward_saints = BLOCK_REWARD * 100_000_000
    reward_saints //= 2 ** halvings

    return reward_saints / 100_000_000