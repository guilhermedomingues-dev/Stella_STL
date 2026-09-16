from core.blockchain import Blockchain
from core.wallet import Wallet
from core.utxo import create_utxo, get_balance

blockchain = Blockchain()

wallet_a = Wallet()
wallet_b = Wallet()

available_utxos = blockchain.available_utxos
spent_utxos = []

utxo = create_utxo(
    "transaction_1",
    0,
    wallet_a.address,
    10
)

available_utxos.append(utxo)

transaction = wallet_a.create_transaction(
    wallet_b.address,
    10,
    available_utxos,
    spent_utxos
)

assert transaction is not None

transaction = wallet_a.sign_transaction(transaction)

assert transaction['outputs'][0]['owner'] == wallet_b.address
assert transaction['outputs'][0]['amount'] == 10

assert get_balance(
    wallet_b.address,
    available_utxos
) == 10

print("Teste de transação em rede concluído com sucesso!")