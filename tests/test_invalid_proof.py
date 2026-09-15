from core.blockchain import Blockchain
from core.block import new_block, hash


blockchain = Blockchain()

last_block = blockchain.last_block

invalid_block = new_block(
    index=last_block['index'] + 1,
    transactions=[],
    proof=1,
    previous_hash=hash(last_block)
)

chain = blockchain.chain + [invalid_block]

assert blockchain.valid_chain(chain) is False

print("Teste de Proof of Work inválida concluído com sucesso!")