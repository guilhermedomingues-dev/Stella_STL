#python -m tests.test_authorized_access

from persistence.user_repository import create_user, get_user_wallet


user = create_user("Guilherme", "senha123")

wallet = get_user_wallet(
    user.user_id,
    user.login_id
)

assert wallet is not None
assert wallet.address == user.wallet.address

print("Teste de acesso autorizado concluído com sucesso!")