"""
Identificação do nó atual na rede.
"""

from uuid import uuid4


def generate_node_id():
    return str(uuid4()).replace('-', '')