from core.transaction import create_coinbase_transaction
from core.mining import valid_coinbase
from config import BLOCK_REWARD


blockchain = []

coinbase = create_coinbase_transaction(
    "wallet_1",
    BLOCK_REWARD + 50
)

assert valid_coinbase(coinbase, blockchain) is False

print("Teste de criação arbitrária de moedas concluído com sucesso!")