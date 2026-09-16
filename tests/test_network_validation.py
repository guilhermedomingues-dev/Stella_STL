from core.blockchain import Blockchain
from core.block import new_block, hash
from core.transaction import valid_transaction
from core.utxo import create_utxo

blockchain = Blockchain()

last_block = blockchain.last_block

proof = blockchain.proof_of_work(last_block['proof'])

valid_block = new_block(
    index=last_block['index'] + 1,
    transactions=[],
    proof=proof,
    previous_hash=hash(last_block)
)

assert blockchain.valid_received_block(valid_block) is True

invalid_block = new_block(
    index=last_block['index'] + 1,
    transactions=[],
    proof=1,
    previous_hash="hash_incorreto"
)

assert blockchain.valid_received_block(invalid_block) is False

utxo = create_utxo(
    "transaction_1",
    0,
    "wallet_1",
    100
)

blockchain.available_utxos.append(utxo)

valid_transaction_data = {
    'inputs': [utxo],
    'outputs': [
        {
            'owner': 'wallet_2',
            'amount': 50
        }
    ]
}

assert valid_transaction(
    valid_transaction_data,
    blockchain.available_utxos
) is True

invalid_transaction = {
    'inputs': [],
    'outputs': [
        {
            'owner': 'wallet_2',
            'amount': -50
        }
    ]
}

assert valid_transaction(
    invalid_transaction,
    blockchain.available_utxos
) is False

print("Teste de validação da rede concluído com sucesso!")