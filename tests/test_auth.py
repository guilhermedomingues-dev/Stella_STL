#python -m tests.test_auth

from core.auth import hash_password, verify_password


password = "senha123"
password_hash = hash_password(password)

assert verify_password(password, password_hash) is True
assert verify_password("senhaerrada", password_hash) is False

print("Teste de autenticação concluído com sucesso!")