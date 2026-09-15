from core.blockchain import Blockchain


blockchain = Blockchain()

original_length = len(blockchain.chain)

invalid_block = {
    'index': blockchain.last_block['index'] + 1,
    'timestamp': blockchain.last_block['timestamp'],
    'transactions': [],
    'proof': 1,
    'previous_hash': 'hash_incorreto'
}

assert blockchain.valid_received_block(invalid_block) is False

assert len(blockchain.chain) == original_length

print("Teste de rejeição de bloco inválido concluído com sucesso!")