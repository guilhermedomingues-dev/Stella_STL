"""
Funções relacionadas ao modelo UTXO da Stella.
"""

from config import SAINTS_PER_STL


def create_utxo(transaction_id, output_index, owner, amount):
    if not valid_amount(amount):
        return None

    return {
        'transaction_id': transaction_id,
        'output_index': output_index,
        'owner': owner,
        'amount': amount,
    }


def consume_utxo(utxo, spent_utxos):
    spent_utxos.append(utxo)


def valid_utxo(utxo, available_utxos):
    return utxo in available_utxos


def get_balance(owner, available_utxos):
    return sum(
        utxo['amount']
        for utxo in available_utxos
        if utxo['owner'] == owner
    )


def valid_amount(amount):
    saints = round(amount * SAINTS_PER_STL)

    return saints > 0 and abs(amount * SAINTS_PER_STL - saints) < 1e-8