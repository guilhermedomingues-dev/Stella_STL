from uuid import uuid4


class User:
    def __init__(self, login_id, username, wallet, password):
        self.user_id = str(uuid4()).replace('-', '')
        self.login_id = login_id
        self.username = username
        self.wallet = wallet
        self.address = wallet.address
        self.password_hash = password