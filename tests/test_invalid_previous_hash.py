from core.blockchain import Blockchain
from core.block import new_block


blockchain = Blockchain()

last_block = blockchain.last_block

invalid_block = new_block(
    index=last_block['index'] + 1,
    transactions=[],
    proof=0,
    previous_hash="hash_incorreto"
)

chain = blockchain.chain + [invalid_block]

assert blockchain.valid_chain(chain) is False

print("Teste de hash anterior incorreto concluído com sucesso!")