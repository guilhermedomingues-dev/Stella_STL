from core.blockchain import Blockchain
from core.block import new_block, hash


blockchain = Blockchain()

genesis = blockchain.chain[0]

proof = blockchain.proof_of_work(genesis['proof'])

second_block = new_block(
    index=2,
    transactions=[],
    proof=proof,
    previous_hash=hash(genesis)
)

longer_chain = [genesis, second_block]

assert blockchain.valid_chain(longer_chain) is True

blockchain.chain = [genesis]

assert blockchain.choose_chain(longer_chain) is True
assert blockchain.chain == longer_chain

print("Teste de escolha da cadeia válida concluído com sucesso!")