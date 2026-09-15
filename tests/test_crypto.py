from core.crypto import generate_private_key, get_public_key, sign_message, verify_signature


message = "Transação de teste"

private_key = generate_private_key()
public_key = get_public_key(private_key)
signature = sign_message(private_key, message)

assert verify_signature(public_key, message, signature) is True

print("Testes de criptografia concluídos com sucesso!")