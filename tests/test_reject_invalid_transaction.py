from core.blockchain import Blockchain
from core.transaction import valid_transaction

blockchain = Blockchain()

invalid_transaction = {
    'inputs': [],
    'outputs': [
        {
            'owner': 'wallet_1',
            'amount': -100
        }
    ]
}

assert valid_transaction(
    invalid_transaction,
    blockchain.available_utxos
) is False

assert invalid_transaction not in blockchain.current_transactions

print("Teste de rejeição de transação inválida concluído com sucesso!")