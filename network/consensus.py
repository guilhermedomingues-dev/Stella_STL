"""
Registro de nós conhecidos e resolução de conflitos entre cadeias.
"""

import requests
from urllib.parse import urlparse


def register_node(self, address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)


def resolve_conflicts(self):
    for node in self.nodes:
        response = requests.get(f'http://{node}/chain')

        if response.status_code != 200:
            continue

        chain = response.json()['chain']

        if self.choose_chain(chain):
            return True

    return False