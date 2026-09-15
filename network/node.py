"""
Identificação do nó atual na rede.
"""

import requests
from uuid import uuid4

class Node:
    def __init__(self):
        self.node_id = str(uuid4()).replace('-', '')
        self.nodes = set()

    def register_node(self, address):
        self.nodes.add(address)

    def broadcast_transaction(self, transaction):
        for node in self.nodes:
            requests.post(
                f'{node}/transactions/receive',
                json=transaction
            )

    def broadcast_block(self, block):
        for node in self.nodes:
            requests.post(
                f'{node}/blocks/receive',
                json=block
            )