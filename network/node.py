"""
Identificação do nó atual na rede.

Versão inicial: apenas gera o identificador único do nó. Registro de peers
e sincronização entre nós serão implementados na FASE 7 (Rede P2P).
"""

from uuid import uuid4

def generate_node_id():
    """
    Gera um identificador único para este nó
    :return: <str> Identificador do nó
    """
    return str(uuid4()).replace('-', '')