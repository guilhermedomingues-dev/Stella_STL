import json
import os
import psycopg
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from core.wallet import Wallet
from core.crypto import get_public_key
from config import MATURATION_BLOCKS


DATABASE_DIR = Path("database")
KEY_PATH = DATABASE_DIR / "wallet.key"


def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])


def get_encryption_key():
    DATABASE_DIR.mkdir(exist_ok=True)

    if not KEY_PATH.exists():
        KEY_PATH.write_bytes(Fernet.generate_key())

    return KEY_PATH.read_bytes()


def get_wallet(address):
    connection = get_connection()

    row = connection.execute(
        "SELECT address, public_key, private_key FROM wallets WHERE address = %s",
        (address,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    encryption = Fernet(get_encryption_key())

    private_key = load_pem_private_key(
        encryption.decrypt(row[2].encode()),
        password=None
    )

    wallet = Wallet.__new__(Wallet)
    wallet.private_key = private_key
    wallet.public_key = get_public_key(private_key)
    wallet.address = row[0]

    return wallet


def save_utxo(utxo):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO utxos (
            transaction_id,
            output_index,
            owner,
            amount
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            utxo['transaction_id'],
            utxo['output_index'],
            utxo['owner'],
            utxo['amount'],
        )
    )

    connection.commit()
    connection.close()


def remove_utxo(utxo):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM utxos
        WHERE transaction_id = %s AND output_index = %s
        """,
        (
            utxo['transaction_id'],
            utxo['output_index'],
        )
    )

    connection.commit()
    connection.close()


def get_utxos():
    connection = get_connection()

    rows = connection.execute(
        "SELECT transaction_id, output_index, owner, amount FROM utxos"
    ).fetchall()

    connection.close()

    return [
        {
            'transaction_id': row[0],
            'output_index': row[1],
            'owner': row[2],
            'amount': row[3],
        }
        for row in rows
    ]


def rebuild_utxos(chain):
    utxos = {}
    current_block_index = chain[-1]['index']

    for block in chain:
        confirmations = current_block_index - block['index']

        for transaction in block['transactions']:
            transaction_id = transaction.get('transaction_id')

            if transaction.get('type') == 'coinbase':
                if confirmations < MATURATION_BLOCKS:
                    continue

            for index, output in enumerate(transaction.get('outputs', [])):
                key = (transaction_id, index)

                utxos[key] = {
                    'transaction_id': transaction_id,
                    'output_index': index,
                    'owner': output['owner'],
                    'amount': output['amount'],
                }

            for utxo in transaction.get('inputs', []):
                key = (
                    utxo['transaction_id'],
                    utxo['output_index']
                )
                utxos.pop(key, None)

    return list(utxos.values())


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS blocks (
            index_number INTEGER PRIMARY KEY,
            timestamp DOUBLE PRECISION NOT NULL,
            transactions TEXT NOT NULL,
            proof INTEGER NOT NULL,
            previous_hash TEXT NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS utxos (
            transaction_id TEXT NOT NULL,
            output_index INTEGER NOT NULL,
            owner TEXT NOT NULL,
            amount DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (transaction_id, output_index)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_wallet(wallet):
    connection = get_connection()
    encryption = Fernet(get_encryption_key())

    private_key = wallet.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    encrypted_private_key = encryption.encrypt(private_key).decode()

    connection.execute(
        """
        INSERT INTO wallets (
            address,
            public_key,
            private_key
        )
        VALUES (%s, %s, %s)
        """,
        (
            wallet.address,
            wallet.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),
            encrypted_private_key,
        )
    )

    connection.commit()
    connection.close()


def save_block(block):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO blocks (
            index_number,
            timestamp,
            transactions,
            proof,
            previous_hash
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            block['index'],
            block['timestamp'],
            json.dumps(block['transactions']),
            block['proof'],
            str(block['previous_hash']),
        )
    )

    connection.commit()
    connection.close()


def get_blocks():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            index_number,
            timestamp,
            transactions,
            proof,
            previous_hash
        FROM blocks
        ORDER BY index_number
        """
    ).fetchall()

    connection.close()

    return [
        {
            'index': row[0],
            'timestamp': row[1],
            'transactions': json.loads(row[2]),
            'proof': row[3],
            'previous_hash': row[4],
        }
        for row in rows
    ]


def get_next_login_id():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS user_sequence (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            next_login_id INTEGER NOT NULL
        )
        """
    )

    connection.execute(
        """
        INSERT INTO user_sequence (id, next_login_id)
        VALUES (1, 1)
        ON CONFLICT (id) DO NOTHING
        """
    )

    login_id = connection.execute(
        "SELECT next_login_id FROM user_sequence WHERE id = 1"
    ).fetchone()[0]

    connection.execute(
        """
        UPDATE user_sequence
        SET next_login_id = next_login_id + 1
        WHERE id = 1
        """
    )

    connection.commit()
    connection.close()

    return login_id