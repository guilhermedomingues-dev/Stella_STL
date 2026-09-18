"""
Funções relacionadas à criação e assinatura de transações.
"""

import hashlib
from core.utxo import valid_utxo, consume_utxo, create_utxo
from core.crypto import sign_message, verify_signature
from config import SAINTS_PER_STL, TRANSACTION_FEE_RATE, MAX_TRANSACTION_FEE
from core.mining import get_block_reward


def create_output(owner, amount):
    return {
        'owner': owner,
        'amount': amount,
    }

def calculate_transaction_fee(amount, block_index):
    reward = get_block_reward(block_index)

    if reward > 0:
        return 0

    amount_saints = round(amount * SAINTS_PER_STL)

    fee_saints = round(
        amount_saints * TRANSACTION_FEE_RATE
    )

    if fee_saints < 1:
        fee_saints = 1

    max_fee_saints = MAX_TRANSACTION_FEE * SAINTS_PER_STL

    if fee_saints > max_fee_saints:
        fee_saints = max_fee_saints

    return fee_saints / SAINTS_PER_STL

def new_transaction(inputs, outputs, available_utxos, spent_utxos, block_index=None):
    for utxo in inputs:
        if not valid_utxo(utxo, available_utxos):
            return None

    if any(not valid_amount(output['amount']) for output in outputs):
        return None

    input_amount = sum(utxo['amount'] for utxo in inputs)
    output_amount = sum(output['amount'] for output in outputs)

    if output_amount > input_amount:
        return None

    fee = 0

    if block_index is not None:
        fee = calculate_transaction_fee(
            output_amount,
            block_index
        )

    total_required = output_amount + fee

    if total_required > input_amount:
        return None

    change = input_amount - total_required

    if change > 0:
        outputs.append(
            create_output(
                inputs[0]['owner'],
                change
            )
        )

    transaction = {
        'inputs': inputs,
        'outputs': outputs,
        'fee': fee,
    }

    transaction['transaction_id'] = hashlib.sha256(
        str(transaction).encode()
    ).hexdigest()

    for utxo in inputs:
        available_utxos.remove(utxo)
        consume_utxo(utxo, spent_utxos)

    for index, output in enumerate(outputs):
        new_utxo = create_utxo(
            transaction['transaction_id'],
            index,
            output['owner'],
            output['amount']
        )

        available_utxos.append(new_utxo)

    return transaction

def valid_transaction(transaction, available_utxos, block_index=None):
    inputs = transaction.get('inputs', [])
    outputs = transaction.get('outputs', [])
    fee = transaction.get('fee', 0)

    if not inputs or not outputs:
        return False

    if any(not valid_amount(output['amount']) for output in outputs):
        return False

    if not valid_amount(fee) and fee != 0:
        return False

    for utxo in inputs:
        if not valid_utxo(utxo, available_utxos):
            return False

    input_amount = sum(utxo['amount'] for utxo in inputs)
    output_amount = sum(output['amount'] for output in outputs)

    if block_index is not None:
        expected_fee = calculate_transaction_fee(
            output_amount,
            block_index
        )

        if fee != expected_fee:
            return False

    if output_amount + fee > input_amount:
        return False

    return True


def sign_transaction(private_key, transaction):
    message = str(transaction)
    signature = sign_message(private_key, message)
    transaction['signature'] = signature.hex()
    return transaction


def verify_transaction(public_key, transaction):
    data = transaction.copy()
    signature = bytes.fromhex(data.pop('signature'))
    message = str(data)
    verify_signature(public_key, message, signature)
    return True


def create_coinbase_transaction(miner_address, reward, block_index):
    return {
        'type': 'coinbase',
        'inputs': [],
        'outputs': [
            {
                'owner': miner_address,
                'amount': reward
            }
        ],
        'transaction_id': hashlib.sha256(
            f'{miner_address}{reward}{block_index}'.encode()
        ).hexdigest(),
        'block_index': block_index
    }

def valid_amount(amount):
    saints = round(amount * SAINTS_PER_STL)

    return saints > 0 and abs(amount * SAINTS_PER_STL - saints) < 1e-8