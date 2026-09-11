"""
Funções relacionadas ao modelo UTXO da Stella.
"""


def create_utxo(transaction_id, output_index, owner, amount):
    # Cria e retorna um UTXO identificando sua origem, proprietário e valor.
    return {
        'transaction_id': transaction_id,
        'output_index': output_index,
        'owner': owner,
        'amount': amount,
    }

def consume_utxo(utxo, spent_utxos):
    # Adiciona o UTXO à lista de UTXOs já consumidos.
    spent_utxos.append(utxo)

def valid_utxo(utxo, available_utxos):
    # Verifica se o UTXO está disponível para ser consumido.
    return utxo in available_utxos

# Calcula o saldo de um proprietário com base nos UTXOs disponíveis.
def get_balance(owner, available_utxos):
    # Soma os valores dos UTXOs pertencentes ao proprietário informado.
    return sum(utxo['amount'] for utxo in available_utxos if utxo['owner'] == owner)