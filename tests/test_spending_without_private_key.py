from core.wallet import Wallet
from core.crypto import verify_signature


wallet = Wallet()

message = "transaction"

fake_signature = b"assinatura_invalida"

try:
    verify_signature(
        wallet.public_key,
        message,
        fake_signature
    )
    valid = True
except Exception:
    valid = False

assert valid is False

print("Teste de gasto sem chave privada concluído com sucesso!")