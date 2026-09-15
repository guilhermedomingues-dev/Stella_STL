from core.utxo import create_utxo, valid_utxo


utxo = create_utxo(
    "transaction_1",
    0,
    "wallet_1",
    100
)

available_utxos = [utxo]

assert valid_utxo(utxo, available_utxos) is True

available_utxos.remove(utxo)

assert valid_utxo(utxo, available_utxos) is False

print("Teste de gasto duplo concluído com sucesso!")