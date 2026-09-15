"""
Registro de nós conhecidos e resolução de conflitos entre cadeias.
"""

import requests
from urllib.parse import urlparse


def register_node(self, address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)


def resolve_conflicts(self):
    neighbours = self.nodes
    new_chain = None
    max_length = len(self.chain)

    for node in neighbours:
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

    if new_chain:
        self.chain = new_chain
        return True

    return False