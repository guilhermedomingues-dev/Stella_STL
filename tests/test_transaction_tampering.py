from core.blockchain import Blockchain


blockchain = Blockchain()

blockchain.current_transactions.append({
    'type': 'test',
    'amount': 100
})

blockchain.add_block(
    proof=100,
    previous_hash=blockchain.last_block['previous_hash']
)

blockchain.chain[-1]['transactions'][0]['amount'] = 500

assert blockchain.valid_chain(blockchain.chain) is False

print("Teste de alteração de transação concluído com sucesso!")