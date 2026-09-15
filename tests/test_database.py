from persistence.database import (
    initialize_database,
    save_block,
    get_blocks,
    save_utxo,
    get_utxos,
    save_wallet,
    get_wallet
)
from core.block import new_block
from core.utxo import create_utxo
from core.wallet import Wallet


initialize_database()

block = new_block(1, [], 300, "hash-teste-recuperacao")
save_block(block)

recovered_blocks = get_blocks()
assert block in recovered_blocks

utxo = create_utxo("transaction-teste", 0, "wallet-teste", 10)
save_utxo(utxo)

recovered_utxos = get_utxos()
assert utxo in recovered_utxos

wallet = Wallet()
save_wallet(wallet)

recovered_wallet = get_wallet(wallet.address)

assert recovered_wallet is not None
assert recovered_wallet.address == wallet.address
assert recovered_wallet.public_key.public_numbers() == wallet.public_key.public_numbers()
assert recovered_wallet.private_key.private_numbers() == wallet.private_key.private_numbers()

print("Teste de recuperação dos dados concluído com sucesso!")