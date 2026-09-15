#python -m tests.test_user

from persistence.user_repository import create_user


user = create_user("Guilherme", "senha123")

assert user.user_id is not None
assert user.login_id is not None
assert user.username == "Guilherme"
assert user.wallet is not None
assert user.address == user.wallet.address

print("Teste de criação de usuário concluído com sucesso!")