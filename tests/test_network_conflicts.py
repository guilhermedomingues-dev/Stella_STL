from core.blockchain import Blockchain
from core.block import new_block, hash

node_1 = Blockchain()
node_2 = Blockchain()

genesis = node_1.chain[0]

proof_1 = node_1.proof_of_work(genesis['proof'])

block_1 = new_block(
    index=2,
    transactions=[],
    proof=proof_1,
    previous_hash=hash(genesis)
)

proof_2 = node_1.proof_of_work(block_1['proof'])

block_2 = new_block(
    index=3,
    transactions=[],
    proof=proof_2,
    previous_hash=hash(block_1)
)

longer_chain = [genesis, block_1, block_2]

node_2.chain = [genesis]

assert len(longer_chain) > len(node_2.chain)
assert node_2.valid_chain(longer_chain) is True
assert node_2.choose_chain(longer_chain) is True
assert node_2.chain == longer_chain

print("Teste de resolução de conflitos concluído com sucesso!")