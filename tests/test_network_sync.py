from core.blockchain import Blockchain
from core.block import hash

node_1 = Blockchain()
node_2 = Blockchain()
node_3 = Blockchain()

block = node_1.add_block(
    proof=node_1.proof_of_work(node_1.last_block['proof']),
    previous_hash=hash(node_1.last_block)
)

node_2.chain.append(block)
node_3.chain.append(block)

assert len(node_1.chain) == len(node_2.chain)
assert len(node_2.chain) == len(node_3.chain)

assert node_1.chain == node_2.chain
assert node_2.chain == node_3.chain

print("Teste de sincronização entre nós concluído com sucesso!")