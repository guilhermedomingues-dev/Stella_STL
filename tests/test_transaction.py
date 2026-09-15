from core.transaction import create_output, new_transaction
from core.utxo import create_utxo, get_balance


def test_transaction():
    available_utxos = [create_utxo("tx0", 0, "Alice", 100)]
    spent_utxos = []
    outputs = [create_output("Bob", 30)]

    transaction = new_transaction(
        available_utxos.copy(),
        outputs,
        available_utxos,
        spent_utxos
    )

    assert transaction is not None
    assert transaction["outputs"][0]["amount"] == 30
    assert transaction["outputs"][1]["amount"] == 70


def test_double_spend():
    available_utxos = [create_utxo("tx0", 0, "Alice", 100)]
    spent_utxos = []

    first_transaction = new_transaction(
        available_utxos.copy(),
        [create_output("Bob", 30)],
        available_utxos,
        spent_utxos
    )

    second_transaction = new_transaction(
        [create_utxo("tx0", 0, "Alice", 100)],
        [create_output("Bob", 30)],
        available_utxos,
        spent_utxos
    )

    assert first_transaction is not None
    assert second_transaction is None


def test_balance():
    available_utxos = [
        create_utxo("tx1", 0, "Alice", 70),
        create_utxo("tx2", 0, "Alice", 20),
        create_utxo("tx3", 0, "Bob", 30)
    ]

    assert get_balance("Alice", available_utxos) == 90
    assert get_balance("Bob", available_utxos) == 30