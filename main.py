"""
Ponto de entrada da aplicação Stella.
"""

from api.app import app
from config import DEFAULT_HOST, DEFAULT_PORT

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
