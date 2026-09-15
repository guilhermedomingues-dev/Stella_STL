"""
Funções relacionadas ao modelo UTXO da Stella.
"""


def create_utxo(transaction_id, output_index, owner, amount):
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