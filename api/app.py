from core.block import new_block, hash
from core.transaction import new_transaction as create_transaction
from core.blockchain import Blockchain
from network.node import generate_node_id
from uuid import uuid4
from core.transaction import valid_transaction

from flask import Flask, jsonify, request

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

available_utxos = []
spent_utxos = []


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block()

    if block is None:
        return 'Invalid proof', 400

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['inputs', 'outputs']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = create_transaction(
        values['inputs'],
        values['outputs'],
        available_utxos,
        spent_utxos
    )

    if transaction is None:
        return 'Invalid transaction', 400

    blockchain.current_transactions.append(transaction)

    index = blockchain.last_block['index'] + 1

    response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
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

@app.route('/transactions/receive', methods=['POST'])
def receive_transaction():
    transaction = request.get_json()

    if not valid_transaction(transaction, blockchain.available_utxos):
        return jsonify({
            'message': 'Invalid transaction'
        }), 400

    blockchain.current_transactions.append(transaction)

    return jsonify({
        'message': 'Transaction received'
    }), 200

@app.route('/blocks/receive', methods=['POST'])
def receive_block():
    block = request.get_json()

    if not blockchain.valid_received_block(block):
        return jsonify({
            'message': 'Invalid block'
        }), 400

    blockchain.chain.append(block)

    return jsonify({
        'message': 'Block received'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)