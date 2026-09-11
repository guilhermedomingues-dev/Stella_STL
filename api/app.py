from core.block import new_block, hash
from core.transaction import new_transaction as create_transaction
from core.blockchain import Blockchain
from network.node import generate_node_id
from uuid import uuid4

from flask import Flask, jsonify, request

# Cria a aplicação Flask que representa o nó da blockchain
app = Flask(__name__)

# Gera um identificador único para identificar este nó na rede
node_identifier = str(uuid4()).replace('-', '')

# Cria uma instância da blockchain que será utilizada por este nó
blockchain = Blockchain()

# Cria a lista de UTXOs disponíveis para serem utilizados nas transações.
available_utxos = []

# Cria a lista de UTXOs que já foram consumidos.
spent_utxos = []

@app.route('/mine', methods=['GET'])
def mine():
    # Executa o PoW usando a prova do último bloco para encontrar a próxima prova
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # O nó recebe uma recompensa por encontrar uma prova válida.
    # O remetente é "0" para indicar que a moeda foi criada como recompensa pela mineração deste bloco.
    
    """transaction = create_transaction("0", node_identifier, 1)"""  # Cria a transação de recompensa pela mineração.
    """blockchain.current_transactions.append(transaction)"""

    # Cria o novo bloco utilizando a prova encontrada e o hash do bloco anterior
    previous_hash = hash(last_block)
    block = blockchain.add_block(proof, previous_hash)

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
    # Obtém os dados enviados na requisição.
    values = request.get_json()

    # Verifica se os campos obrigatórios foram enviados.
    required = ['inputs', 'outputs']
    if not all(k in values for k in required):
        # Retorna erro caso algum campo obrigatório esteja ausente.
        return 'Missing values', 400

    # Cria a transação utilizando os UTXOs disponíveis e gastos.
    transaction = create_transaction(
        values['inputs'],
        values['outputs'],
        available_utxos,
        spent_utxos
    )

    # Verifica se a transação foi rejeitada.
    if transaction is None:
        # Retorna erro caso os UTXOs ou valores sejam inválidos.
        return 'Invalid transaction', 400

    # Adiciona a transação válida à lista de transações pendentes.
    blockchain.current_transactions.append(transaction)

    # Calcula o índice do próximo bloco que receberá a transação.
    index = blockchain.last_block['index'] + 1

    # Cria a resposta informando o bloco da transação.
    response = {'message': f'Transaction will be added to Block {index}'}

    # Retorna a resposta em formato JSON com status 201.
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