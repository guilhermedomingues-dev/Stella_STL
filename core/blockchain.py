"""
Classe responsável por gerenciar a blockchain e sua cadeia de blocos.
"""

import hashlib
import json
from time import time

from core.block import new_block, hash, valid_block
from core.transaction import new_transaction
from core.mining import valid_proof

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        self.chain.append(new_block(index=1, transactions=[], proof=100, previous_hash=1))

    def new_block(self, index, proof, previous_hash=None):
        """
        Cria um novo bloco e o adiciona à blockchain
        """
        block = {
            'index': index,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Limpa a lista de transações pendentes após incluí-las no novo bloco
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adiciona uma nova transação à lista de transações pendentes
        :param sender: <str> Endereço de quem está enviando
        :param recipient: <str> Endereço de quem está recebendo
        :param amount: <int> Quantidade transferida
        :return: <int> Índice do bloco que receberá essa transação
        """
        self.current_transactions.append(new_transaction(sender, recipient, amount))
        return self.last_block['index'] + 1

    def valid_chain(self, chain):
        """
        Verifica se uma determinada blockchain é válida
        :param chain: <list> Blockchain que será validada
        :return: <bool> True se a blockchain for válida e False caso contrário
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if not valid_block(block):
                return False  # Rejeita a cadeia se o bloco tiver uma estrutura inválida

            # Verifica se o hash anterior armazenado no bloco corresponde ao hash do bloco anterior
            if block['previous_hash'] != hash(last_block):
                return False

            # Verifica se a Proof of Work armazenada no bloco é válida
            if not valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def proof_of_work(self, last_proof):
        """
        Executa um algoritmo simples de PoW:
         - Procura um número p' cujo hash de p + p' comece com quatro zeros
         - p representa a prova anterior e p' representa a nova prova que estamos procurando
        :param last_proof: <int> Prova encontrada no bloco anterior
        :return: <int> Nova prova encontrada pelo algoritmo
        """

        proof = 0
        while valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
            """
            Gera o hash SHA-256 de um bloco
            :param block: <dict> Bloco que será transformado em hash
            :return: <str> Hash do bloco
            """

            # Garante que as chaves do dicionário sejam ordenadas para que o mesmo bloco sempre gere o mesmo hash
            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
