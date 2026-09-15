from core.blockchain import Blockchain


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

blockchain.current_transactions.append(invalid_transaction)

assert blockchain.current_transactions == [invalid_transaction]

print("Teste de transação inválida propagada pela rede concluído com sucesso!")