from core.blockchain import Blockchain


blockchain = Blockchain()

blockchain.add_block(
    proof=100,
    previous_hash=blockchain.last_block['previous_hash']
)

original_chain = blockchain.chain.copy()

blockchain.chain[0]['transactions'].append({
    'type': 'test',
    'amount': 100
})

assert blockchain.valid_chain(blockchain.chain) is False

blockchain.chain = original_chain

print("Teste de alteração de bloco antigo concluído com sucesso!")