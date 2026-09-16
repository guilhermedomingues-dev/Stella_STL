from persistence.user_repository import create_user, get_user
from core.auth import verify_password

user = create_user("Guilherme", "senha123")

stored_user = get_user(user.login_id)

assert stored_user is not None
assert stored_user[0] == user.user_id
assert stored_user[1] == user.login_id
assert stored_user[2] == user.username
assert verify_password("senha123", stored_user[4]) is True
assert verify_password("senhaerrada", stored_user[4]) is False

print("Teste de autenticação de usuário concluído com sucesso!")