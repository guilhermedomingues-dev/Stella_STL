#python -m tests.test_unauthorized_access

from persistence.user_repository import create_user, get_user_wallet


user_1 = create_user("Guilherme", "senha123")
user_2 = create_user("João", "senha456")

wallet = get_user_wallet(
    user_1.user_id,
    user_2.login_id
)

assert wallet is None

print("Teste de acesso não autorizado concluído com sucesso!")