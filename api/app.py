from core.block import new_block, hash
from core.transaction import new_transaction as create_transaction, valid_transaction
from core.blockchain import Blockchain
from uuid import uuid4
from persistence.user_repository import create_user, get_user_wallet, get_user
from core.utxo import get_balance
from core.auth import verify_password
from persistence.database import remove_utxo

from flask import Flask, jsonify, request, render_template, session, redirect, flash

app = Flask(__name__)

app.secret_key = 'stella-secret-key'

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

available_utxos = []
spent_utxos = []


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']

    user = create_user(username, password)

    return jsonify({
        'message': 'User created',
        'user_id': user.user_id,
        'login_id': user.login_id,
        'username': user.username,
        'address': user.address
    }), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    login_id = request.form['login_id']
    password = request.form['password']

    user = get_user(login_id)

    if user is None:
        return 'Login ID ou senha inválidos', 401

    if not verify_password(password, user[4]):
        return 'Login ID ou senha inválidos', 401

    session['user_id'] = user[0]
    session['login_id'] = user[1]
    session['username'] = user[2]

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        username=session['username'],
        login_id=session['login_id'],
        user_id=session['user_id']
    )

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        'account.html',
        username=session['username'],
        login_id=session['login_id']
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/wallet')
def wallet():
    if 'user_id' not in session:
        return redirect('/login')

    wallet = get_user_wallet(
        session['user_id'],
        session['login_id']
    )

    if wallet is None:
        return 'Wallet not found', 404

    return render_template(
        'wallet.html',
        address=wallet.address
    )

@app.route('/balance')
def balance():
    if 'user_id' not in session:
        return redirect('/login')

    wallet = get_user_wallet(
        session['user_id'],
        session['login_id']
    )

    if wallet is None:
        return 'Wallet not found', 404

    balance = get_balance(
        wallet.address,
        blockchain.available_utxos
    )

    return render_template(
        'balance.html',
        balance=balance,
        address=wallet.address
    )

@app.route('/send', methods=['GET', 'POST'])
def send():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'GET':
        return render_template('send.html')

    recipient_id = int(request.form['recipient'])
    amount = float(request.form['amount'])

    wallet = get_user_wallet(
        session['user_id'],
        session['login_id']
    )

    if wallet is None:
        return 'Wallet not found', 404

    recipient = get_user(recipient_id)

    if recipient is None:
        return 'Recipient not found', 404

    recipient_wallet = get_user_wallet(
        recipient[0],
        recipient[1]
    )

    if recipient_wallet is None:
        return 'Recipient wallet not found', 404

    transaction = wallet.create_transaction(
        recipient_wallet.address,
        amount,
        blockchain.available_utxos,
        spent_utxos
    )

    if transaction is None:
        return 'Invalid transaction', 400

    transaction = wallet.sign_transaction(transaction)

    blockchain.current_transactions.append(transaction)

    return jsonify({
        'message': 'Transaction received',
        'transaction': transaction
    }), 201

@app.route('/receive')
def receive():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        'receive.html',
        login_id=session['login_id']
    )

@app.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect('/login')

    wallet = get_user_wallet(
        session['user_id'],
        session['login_id']
    )

    if wallet is None:
        return 'Wallet not found', 404

    transactions = []

    for block in blockchain.chain:
        for transaction in block['transactions']:
            for output in transaction.get('outputs', []):
                if output.get('owner') == wallet.address:
                    transactions.append(transaction)
                    break

    return render_template(
        'transactions.html',
        transactions=transactions
    )

@app.route('/blocks')
def blocks():
    if 'user_id' not in session:
        return redirect('/login')

    index = request.args.get('index')

    if index is None:
        return render_template('blocks.html')

    block = next(
        (
            block
            for block in blockchain.chain
            if block['index'] == int(index)
        ),
        None
    )

    if block is None:
        return 'Block not found', 404

    return render_template(
        'blocks.html',
        block=block
    )

@app.route('/mine', methods=['GET', 'POST'])
def mine():
    if 'user_id' not in session:
        return redirect('/login')

    wallet = get_user_wallet(
        session['user_id'],
        session['login_id']
    )

    if wallet is None:
        return 'Wallet not found', 404

    if request.method == 'GET':
        return render_template(
            'mining.html',
            address=wallet.address
        )

    block = blockchain.mine_block(wallet.address)

    if block is None:
        return 'Invalid proof', 400

    return render_template(
        'mining.html',
        address=wallet.address,
        message=f'Bloco {block["index"]} minerado com sucesso!'
    )


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['inputs', 'outputs']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = create_transaction(
        values['inputs'],
        values['outputs'],
        blockchain.available_utxos,
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

    if blockchain.mempool_full():
        return jsonify({
            'message': 'Mempool is full'
        }), 400

    if not valid_transaction(transaction, blockchain.available_utxos):
        return jsonify({
            'message': 'Invalid transaction'
        }), 400

    for utxo in transaction['inputs']:
        blockchain.available_utxos.remove(utxo)
        remove_utxo(utxo)

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

    blockchain.receive_block(block)

    return jsonify({
        'message': 'Block received'
    }), 200

@app.route('/users', methods=['POST'])
def create_user_api():
    values = request.get_json()

    required = ['username', 'password']

    if not all(k in values for k in required):
        return 'Missing values', 400

    user = create_user(
        values['username'],
        values['password']
    )

    response = {
        'message': 'User created',
        'user_id': user.user_id,
        'login_id': user.login_id,
        'username': user.username,
        'address': user.address
    }

    return jsonify(response), 201

@app.route('/wallet/<user_id>/<int:login_id>', methods=['GET'])
def get_wallet_api(user_id, login_id):
    wallet = get_user_wallet(user_id, login_id)

    if wallet is None:
        return jsonify({
            'message': 'Wallet not found'
        }), 404

    return jsonify({
        'address': wallet.address
    }), 200

@app.route('/wallet/<user_id>/<int:login_id>/balance', methods=['GET'])
def get_wallet_balance(user_id, login_id):
    wallet = get_user_wallet(user_id, login_id)

    if wallet is None:
        return jsonify({
            'message': 'Wallet not found'
        }), 404

    balance = get_balance(
        wallet.address,
        blockchain.available_utxos
    )

    return jsonify({
        'address': wallet.address,
        'balance': balance
    }), 200

@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    for block in blockchain.chain:
        for transaction in block['transactions']:
            if transaction.get('transaction_id') == transaction_id:
                return jsonify(transaction), 200

    return jsonify({
        'message': 'Transaction not found'
    }), 404

@app.route('/blocks/<int:index>', methods=['GET'])
def get_block(index):
    for block in blockchain.chain:
        if block['index'] == index:
            return jsonify(block), 200

    return jsonify({
        'message': 'Block not found'
    }), 404

@app.route('/transactions/send', methods=['POST'])
def send_stl():
    values = request.get_json()

    required = ['user_id', 'login_id', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    wallet = get_user_wallet(
        values['user_id'],
        values['login_id']
    )

    if wallet is None:
        return jsonify({
            'message': 'Wallet not found'
        }), 404

    transaction = wallet.create_transaction(
        values['recipient'],
        values['amount'],
        blockchain.available_utxos,
        blockchain.spent_utxos
    )

    if transaction is None:
        return jsonify({
            'message': 'Invalid transaction'
        }), 400

    transaction = wallet.sign_transaction(transaction)

    blockchain.current_transactions.append(transaction)

    return jsonify({
        'message': 'Transaction received',
        'transaction': transaction
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)