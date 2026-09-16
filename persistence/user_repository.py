from core.user import User
from core.wallet import Wallet
from persistence.database import (
    get_connection,
    get_next_login_id,
    save_wallet,
    get_wallet,
    initialize_database
)
from core.auth import hash_password


class AuthenticatedUser:
    def __init__(self, user):
        self.user_id = user.user_id
        self.login_id = user.login_id
        self.wallet = user.wallet


def create_user(username, password):
    initialize_database()

    login_id = get_next_login_id()
    wallet = Wallet()
    password_hash = hash_password(password)
    user = User(login_id, username, wallet, password_hash)

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            login_id INTEGER UNIQUE NOT NULL,
            username TEXT NOT NULL,
            wallet_address TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    connection.execute(
        """
        INSERT INTO users (
            user_id,
            login_id,
            username,
            wallet_address,
            password_hash
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user.user_id,
            user.login_id,
            user.username,
            user.wallet.address,
            password_hash,
        )
    )

    connection.commit()
    connection.close()

    save_wallet(wallet)

    return user


def get_user(login_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT user_id, login_id, username, wallet_address, password_hash
        FROM users
        WHERE login_id = ?
        """,
        (login_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return row


def get_user_wallet(user_id, login_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT wallet_address
        FROM users
        WHERE user_id = ? AND login_id = ?
        """,
        (user_id, login_id)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return get_wallet(row[0])