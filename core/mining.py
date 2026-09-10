"""
Algoritmo de Proof of Work (PoW) da MariaCoin.

Versão inicial. Será integrada às regras monetárias (recompensa, coinbase)
na FASE 6.
"""

import hashlib

def proof_of_work(last_proof):
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

def valid_proof(last_proof, proof):
        """
        Verifica se a PoW é válida.
        :param last_proof: <int> Prova encontrada no bloco anterior
        :param proof: <int> Prova que está sendo verificada
        :return: <bool> True se a prova for válida e False caso contrário
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"