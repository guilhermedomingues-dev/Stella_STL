"""
Registro de nós conhecidos e resolução de conflitos entre cadeias.

Versão inicial de consenso. Será transformada em regras completas do
protocolo (validação de blocos/transações recebidas, etc.) na FASE 8.
"""

import requests
from urllib.parse import urlparse

def register_node(self, address):
        """
        Adiciona um novo nó à lista de nós conhecidos pela blockchain
        :param address: <str> Endereço do nó. Ex.: 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

def resolve_conflicts(self):
        """
        Executa o algoritmo de consenso, substituindo nossa cadeia pela maior cadeia válida encontrada na rede
        :return: <bool> True se nossa cadeia foi substituída e False caso contrário
        """

        neighbours = self.nodes
        new_chain = None

        # Procura apenas por cadeias que sejam maiores que a nossa
        max_length = len(self.chain)

        # Consulta as cadeias dos nós da rede e verifica quais são válidas
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Verifica se a cadeia recebida é maior que a nossa e se passou na validação
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Substitui nossa cadeia caso seja encontrada uma cadeia válida e maior
        if new_chain:
            self.chain = new_chain
            return True

        return False