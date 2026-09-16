from core.blockchain import Blockchain
from core.block import hash

node = Blockchain()

proof = node.proof_of_work(node.last_block['proof'])

block = node.add_block(
    proof=proof,
    previous_hash=hash(node.last_block)
)

saved_chain = node.chain.copy()

del node

restarted_node = Blockchain()

assert restarted_node.chain == saved_chain

print("Teste de persistência da rede concluído com sucesso!")