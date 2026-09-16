from core.blockchain import Blockchain

blockchain = Blockchain()

initial_length = len(blockchain.chain)

block = blockchain.mine_block("miner_wallet")

assert block is not None
assert len(blockchain.chain) == initial_length + 1
assert block['transactions'][0]['type'] == 'coinbase'
assert block['transactions'][0]['outputs'][0]['owner'] == "miner_wallet"

print("Teste de mineração em rede concluído com sucesso!")