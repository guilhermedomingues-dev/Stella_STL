from core.crypto import generate_private_key, get_public_key
from cryptography.hazmat.primitives import serialization, hashes
from config import SAINTS_PER_STL


class Wallet:
    def __init__(self):
        self.private_key = generate_private_key()
        self.public_key = get_public_key(self.private_key)
        self.address = self.generate_address()

    def recover_public_key(self):
        return get_public_key(self.private_key)

    def generate_address(self):
        public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint
        )

        digest = hashes.Hash(hashes.SHA256())
        digest.update(public_key)

        return digest.finalize().hex()

    def get_balance(self, available_utxos):
        return sum(
            utxo['amount']
            for utxo in available_utxos
            if utxo['owner'] == self.address
        )

    def create_transaction(self, recipient, amount, available_utxos, spent_utxos, block_index=None):
        if amount <= 0:
            return None

        saints = round(amount * SAINTS_PER_STL)

        if abs(amount * SAINTS_PER_STL - saints) >= 1e-8:
            return None

        inputs = [
            utxo
            for utxo in available_utxos
            if utxo['owner'] == self.address
        ]

        if not inputs:
            return None

        from core.transaction import new_transaction

        outputs = [
            {
                'owner': recipient,
                'amount': amount
            }
        ]

        return new_transaction(
            inputs,
            outputs,
            available_utxos,
            spent_utxos,
            block_index
        )

    def sign_transaction(self, transaction):
        from core.transaction import sign_transaction

        return sign_transaction(self.private_key, transaction)