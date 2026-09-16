from core.blockchain import Blockchain
from core.transaction import valid_transaction
from core.utxo import create_utxo
from core.block import new_block, hash

blockchain = Blockchain()

utxo = create_utxo(
    "transaction_1",
    0,
    "wallet_1",
    100
)

blockchain.available_utxos.append(utxo)

invalid_transaction = {
    'inputs': [utxo],
    'outputs': [
        {
            'owner': 'wallet_2',
            'amount': 150
        }
    ]
}

assert valid_transaction(
    invalid_transaction,
    blockchain.available_utxos
) is False

invalid_block = new_block(
    index=blockchain.last_block['index'] + 1,
    transactions=[],
    proof=1,
    previous_hash=hash(blockchain.last_block)
)

assert blockchain.valid_received_block(invalid_block) is False

tampered_chain = blockchain.chain.copy()
tampered_chain[0]['transactions'].append({
    'type': 'invalid',
    'amount': 1000
})

assert blockchain.valid_chain(tampered_chain) is False

print("Teste de segurança da rede concluído com sucesso!")