"""
Classe responsável por gerenciar a blockchain e sua cadeia de blocos.
"""

from core.block import new_block, hash, valid_block
from core.transaction import new_transaction
from core.mining import valid_proof


class Blockchain(object):
    # Define a classe responsável por gerenciar a blockchain.
    def __init__(self):
        # Cria a lista de transações pendentes.
        self.current_transactions = []
        # Cria a lista que armazenará os blocos da blockchain.
        self.chain = []
        # Cria o conjunto que armazenará os nós conhecidos.
        self.nodes = set()
        # Cria o bloco gênese da blockchain.
        self.chain.append(new_block(index=1, transactions=[], proof=100, previous_hash=1))

    def add_block(self, proof, previous_hash=None):
        # Cria um novo bloco com as transações pendentes.
        block = new_block(
            index=len(self.chain) + 1,
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash
        )
        # Limpa a lista de transações pendentes após adicioná-las ao bloco.
        self.current_transactions = []
        # Adiciona o novo bloco à blockchain.
        self.chain.append(block)
        # Retorna o bloco criado.
        return block

    def valid_chain(self, chain):
        # Verifica se uma determinada blockchain é válida.
        last_block = chain[0]
        # Inicia a verificação a partir do segundo bloco.
        current_index = 1

        # Percorre todos os blocos restantes da blockchain.
        while current_index < len(chain):
            # Obtém o bloco atual que será verificado.
            block = chain[current_index]

            # Verifica se a estrutura do bloco é válida.
            if not valid_block(block):
                return False

            # Verifica se o hash anterior corresponde ao bloco anterior.
            if block['previous_hash'] != hash(last_block):
                return False

            # Verifica se a prova de trabalho do bloco é válida.
            if not valid_proof(last_block['proof'], block['proof']):
                return False

            # Define o bloco atual como o bloco anterior da próxima verificação.
            last_block = block
            # Avança para o próximo bloco.
            current_index += 1

        # Retorna verdadeiro quando toda a cadeia é válida.
        return True

    def proof_of_work(self, last_proof):
        # Inicia a busca por uma prova válida.
        proof = 0

        # Continua procurando enquanto a prova não for válida.
        while valid_proof(last_proof, proof) is False:
            # Incrementa a prova para testar um novo valor.
            proof += 1

        # Retorna a prova válida encontrada.
        return proof

    @property
    def last_block(self):
        # Retorna o último bloco da blockchain.
        return self.chain[-1]