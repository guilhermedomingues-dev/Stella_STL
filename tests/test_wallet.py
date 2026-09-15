from core.wallet import Wallet
from core.crypto import verify_signature


wallet_1 = Wallet()
wallet_2 = Wallet()

assert wallet_1.private_key != wallet_2.private_key
assert wallet_1.public_key != wallet_2.public_key
assert wallet_1.address != wallet_2.address

recovered_public_key = wallet_1.recover_public_key()

assert recovered_public_key.public_numbers() == wallet_1.public_key.public_numbers()

transaction = {
    'sender': wallet_1.address,
    'recipient': wallet_2.address,
    'amount': 12
}

signed_transaction = wallet_1.sign_transaction(transaction)

signature = bytes.fromhex(signed_transaction['signature'])

transaction_data = signed_transaction.copy()
transaction_data.pop('signature')

message = str(transaction_data)

assert verify_signature(wallet_1.public_key, message, signature) is True

print("Testes da carteira concluídos com sucesso!")