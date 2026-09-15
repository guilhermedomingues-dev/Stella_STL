from core.transaction import new_transaction
from core.utxo import create_utxo


utxo = create_utxo(
    "transaction_1",
    0,
    "wallet_1",
    100
)

available_utxos = [utxo]
spent_utxos = []

transaction = new_transaction(
    [utxo],
    [{'owner': 'wallet_2', 'amount': -50}],
    available_utxos,
    spent_utxos
)

assert transaction is None

print("Teste de envio de valor inválido concluído com sucesso!")