import requests
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse

from flask import Flask, jsonify, request


# Classe responsável por gerenciar a blockchain e sua cadeia de blocos
class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Cria o primeiro bloco da blockchain, conhecido como bloco gênesis
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco e o adiciona à blockchain
        :param proof: <int> Prova encontrada pelo algoritmo de PoW
        :param previous_hash: (Opcional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco criado
        """
        block = {
            'index': len(self.chain) + 1,
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
        Cria uma nova transação para ser incluída no próximo bloco minerado
        :param sender: <str> Endereço de quem está enviando
        :param recipient: <str> Endereço de quem está recebendo
        :param amount: <int> Quantidade transferida
        :return: <int> Índice do bloco que receberá essa transação
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Executa um algoritmo simples de PoW:
         - Procura um número p' cujo hash de p + p' comece com quatro zeros
         - p representa a prova anterior e p' representa a nova prova que estamos procurando
        :param last_proof: <int> Prova encontrada no bloco anterior
        :return: <int> Nova prova encontrada pelo algoritmo
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def register_node(self, address):
        """
        Adiciona um novo nó à lista de nós conhecidos pela blockchain
        :param address: <str> Endereço do nó. Ex.: 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

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
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            
            # Verifica se o hash anterior armazenado no bloco corresponde ao hash do bloco anterior
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Verifica se a Proof of Work armazenada no bloco é válida
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

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

    @staticmethod
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

# Cria a aplicação Flask que representa o nó da blockchain
app = Flask(__name__)

# Gera um identificador único para identificar este nó na rede
node_identifier = str(uuid4()).replace('-', '')

# Cria uma instância da blockchain que será utilizada por este nó
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Executa o PoW usando a prova do último bloco para encontrar a próxima prova
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # O nó recebe uma recompensa por encontrar uma prova válida.
    # O remetente é "0" para indicar que a moeda foi criada como recompensa pela mineração deste bloco.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Cria o novo bloco utilizando a prova encontrada e o hash do bloco anterior
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Verifica se todos os campos obrigatórios foram enviados na requisição
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Cria uma nova transação e informa em qual bloco ela será incluída
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)