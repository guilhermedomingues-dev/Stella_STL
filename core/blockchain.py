"""
Classe responsável por gerenciar a blockchain e sua cadeia de blocos.
"""

from core.block import new_block, hash
from core.transaction import new_transaction
from core.mining import valid_proof

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Cria o primeiro bloco da blockchain, conhecido como bloco gênesis
        self.chain.append(new_block(index=1, transactions=[], proof=100, previous_hash=1))

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco e o adiciona à blockchain
        :param proof: <int> Prova encontrada pelo algoritmo de PoW
        :param previous_hash: (Opcional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco criado
        """
        block = new_block(
            index=len(self.chain) + 1,
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or hash_block(self.chain[-1]),
        )

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

            # Verifica se o hash anterior armazenado no bloco corresponde ao hash do bloco anterior
            if block['previous_hash'] != hash_block(last_block):
                return False

            # Verifica se a Proof of Work armazenada no bloco é válida
            if not valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    @property
    def last_block(self):
        return self.chain[-1]