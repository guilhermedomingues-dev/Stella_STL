from core.utxo import create_utxo, get_balance


utxo = create_utxo(
    "transaction_1",
    0,
    "wallet_1",
    100
)

available_utxos = [utxo]

balance = get_balance(
    "wallet_1",
    available_utxos
)

assert balance == 100

balance = 1000

assert get_balance(
    "wallet_1",
    available_utxos
) == 100

print("Teste de manipulação de saldo concluído com sucesso!")