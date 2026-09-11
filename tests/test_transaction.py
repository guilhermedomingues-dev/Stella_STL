# Importa as funções de transação que serão testadas.
from core.transaction import create_output, new_transaction

# Importa as funções de gerenciamento de UTXOs que serão testadas.
from core.utxo import create_utxo, get_balance


# Cria um teste para verificar a criação de uma transação.
def test_transaction():
    # Cria um UTXO de 100 STL pertencente a Alice.
    available_utxos = [create_utxo("tx0", 0, "Alice", 100)]

    # Cria a lista de UTXOs já consumidos.
    spent_utxos = []

    # Cria um output de 30 STL para Bob.
    outputs = [create_output("Bob", 30)]

    # Cria a transação utilizando o UTXO de Alice.
    transaction = new_transaction(
        available_utxos.copy(),
        outputs,
        available_utxos,
        spent_utxos
    )

    # Verifica se a transação foi criada.
    assert transaction is not None

    # Verifica se o output de Bob possui 30 STL.
    assert transaction["outputs"][0]["amount"] == 30

    # Verifica se o troco de Alice foi criado com 70 STL.
    assert transaction["outputs"][1]["amount"] == 70


# Cria um teste para verificar a prevenção de double-spend.
def test_double_spend():
    # Cria um UTXO de 100 STL pertencente a Alice.
    available_utxos = [create_utxo("tx0", 0, "Alice", 100)]

    # Cria a lista de UTXOs já consumidos.
    spent_utxos = []

    # Cria a primeira transação usando o UTXO.
    first_transaction = new_transaction(
        available_utxos.copy(),
        [create_output("Bob", 30)],
        available_utxos,
        spent_utxos
    )

    # Tenta usar novamente o mesmo UTXO.
    second_transaction = new_transaction(
        [create_utxo("tx0", 0, "Alice", 100)],
        [create_output("Bob", 30)],
        available_utxos,
        spent_utxos
    )

    # Verifica se a primeira transação foi aceita.
    assert first_transaction is not None

    # Verifica se a segunda transação foi rejeitada.
    assert second_transaction is None


# Cria um teste para verificar o cálculo de saldo.
def test_balance():
    # Cria dois UTXOs pertencentes a Alice.
    available_utxos = [
        create_utxo("tx1", 0, "Alice", 70),
        create_utxo("tx2", 0, "Alice", 20),
        create_utxo("tx3", 0, "Bob", 30)
    ]

    # Verifica se o saldo de Alice é 90 STL.
    assert get_balance("Alice", available_utxos) == 90

    # Verifica se o saldo de Bob é 30 STL.
    assert get_balance("Bob", available_utxos) == 30