"""
Classe responsável por gerenciar a blockchain e sua cadeia de blocos.
"""

from core.block import new_block, hash, valid_block
from core.mining import valid_coinbase, valid_proof, get_difficulty, get_block_reward
from config import MATURATION_BLOCKS, MEMPOOL_LIMIT
from persistence.database import (
    initialize_database,
    get_blocks,
    save_block,
    get_utxos,
    save_utxo,
    remove_utxo,
    rebuild_utxos,
    get_mempool_transactions,
    save_mempool_transaction,
    remove_mempool_transaction,
    replace_utxos,
    clear_mempool,
    replace_blocks
)
from core.transaction import create_coinbase_transaction, valid_transaction
from core.utxo import create_utxo
from network.node import Node
from network.consensus import register_node, resolve_conflicts


class Blockchain:
    def __init__(self):
        initialize_database()
        self.chain = get_blocks()
        self.current_transactions = get_mempool_transactions()
        self.available_utxos = get_utxos()
        self.nodes = set()
        self.node = Node()
        self.node.nodes = self.nodes
        self.spent_utxos = []

        if not self.chain:
            self.chain.append(
                new_block(
                    index=1,
                    transactions=[],
                    proof=100,
                    previous_hash=1
                )
            )
            save_block(self.chain[0])

        for transaction in self.current_transactions:
            for utxo in transaction.get('inputs', []):
                if utxo in self.available_utxos:
                    self.available_utxos.remove(utxo)

                self.spent_utxos.append(utxo)

            for index, output in enumerate(transaction.get('outputs', [])):
                utxo = create_utxo(
                    transaction['transaction_id'],
                    index,
                    output['owner'],
                    output['amount']
                )

                if utxo not in self.available_utxos:
                    self.available_utxos.append(utxo)

    def process_confirmed_transactions(self, transactions):
        for transaction in transactions:
            if transaction.get('type') == 'coinbase':
                continue

            for utxo in transaction.get('inputs', []):
                remove_utxo(utxo)

            for index, output in enumerate(transaction.get('outputs', [])):
                utxo = create_utxo(
                    transaction['transaction_id'],
                    index,
                    output['owner'],
                    output['amount']
                )

                if utxo not in self.available_utxos:
                    self.available_utxos.append(utxo)

                save_utxo(utxo)

            remove_mempool_transaction(
                transaction['transaction_id']
            )

    def add_block(self, proof, previous_hash=None):
        valid_transactions = list(self.current_transactions)

        block = new_block(
            index=len(self.chain) + 1,
            transactions=valid_transactions,
            proof=proof,
            previous_hash=previous_hash
        )

        self.chain.append(block)
        save_block(block)
        self.process_confirmed_transactions(block['transactions'])
        self.current_transactions = []
        self.process_matured_coinbases()
        self.node.broadcast_block(block)

        return block

    def receive_block(self, block):
        self.chain.append(block)
        save_block(block)
        self.process_confirmed_transactions(block['transactions'])
        self.process_matured_coinbases()

    def process_matured_coinbases(self):
        current_block_index = self.last_block['index']

        for block in self.chain:
            confirmations = current_block_index - block['index']

            if confirmations < MATURATION_BLOCKS:
                continue

            for transaction in block['transactions']:
                if transaction.get('type') != 'coinbase':
                    continue

                if 'transaction_id' not in transaction:
                    continue

                utxo = create_utxo(
                    transaction['transaction_id'],
                    0,
                    transaction['outputs'][0]['owner'],
                    transaction['outputs'][0]['amount']
                )

                if utxo not in self.available_utxos:
                    self.available_utxos.append(utxo)
                    save_utxo(utxo)

    def _valid_block_transactions(self, block, previous_chain, available_utxos):
        transactions = block.get('transactions')

        if not isinstance(transactions, list) or not transactions:
            return False

        coinbase_transactions = [
            transaction
            for transaction in transactions
            if transaction.get('type') == 'coinbase'
        ]

        if len(coinbase_transactions) != 1:
            return False

        if transactions[0].get('type') != 'coinbase':
            return False

        if not valid_coinbase(
            transactions[0],
            previous_chain,
            block['index'],
            transactions
        ):
            return False

        for transaction in transactions[1:]:
            if transaction.get('type') == 'coinbase':
                return False

            if not valid_transaction(
                transaction,
                available_utxos,
                block['index']
            ):
                return False

            for utxo in transaction['inputs']:
                available_utxos.remove(utxo)

            for index, output in enumerate(transaction['outputs']):
                available_utxos.append(
                    create_utxo(
                        transaction['transaction_id'],
                        index,
                        output['owner'],
                        output['amount']
                    )
                )

        return True

    def _get_validation_utxos(self, chain):
        available_utxos = []

        for block in chain:
            for transaction in block.get('transactions', []):
                if transaction.get('type') == 'coinbase':
                    confirmations = chain[-1]['index'] - block['index']

                    if confirmations < MATURATION_BLOCKS:
                        continue

                for index, output in enumerate(
                    transaction.get('outputs', [])
                ):
                    available_utxos.append(
                        create_utxo(
                            transaction['transaction_id'],
                            index,
                            output['owner'],
                            output['amount']
                        )
                    )

                for utxo in transaction.get('inputs', []):
                    if utxo in available_utxos:
                        available_utxos.remove(utxo)

        return available_utxos

    def valid_chain(self, chain):
        if not chain:
            return False
    
        last_block = chain[0]
    
        if not valid_block(last_block):
            return False
    
        current_index = 1
        available_utxos = self._get_validation_utxos(chain[:1])
    
        while current_index < len(chain):
            block = chain[current_index]
    
            if not valid_block(block):
                return False
    
            if block['previous_hash'] != hash(last_block):
                return False
    
            difficulty = get_difficulty(chain[:current_index])
    
            if not valid_proof(
                last_block['proof'],
                block['proof'],
                difficulty
            ):
                return False
    
            if not valid_coinbase(
                block['transactions'][0],
                chain[:current_index],
                block['index'],
                block['transactions']
            ):
                return False
    
            validation_utxos = list(available_utxos)
    
            if not self._valid_block_transactions(
                block,
                chain[:current_index],
                validation_utxos
            ):
                return False
    
            available_utxos = validation_utxos
            last_block = block
            current_index += 1

        return True

    def get_chain_work(self, chain):
        work = 0

        for index in range(1, len(chain)):
            difficulty = get_difficulty(chain[:index + 1])
            work += 2 ** difficulty

        return work

    def restore_orphaned_transactions(self, old_chain, new_chain):
        new_transaction_ids = {
            transaction.get('transaction_id')
            for block in new_chain
            for transaction in block['transactions']
        }

        transactions = list(self.current_transactions)

        for block in old_chain:
            for transaction in block['transactions']:
                if transaction.get('type') == 'coinbase':
                    continue

                transaction_id = transaction.get('transaction_id')

                if transaction_id in new_transaction_ids:
                    continue

                if transaction not in transactions:
                    transactions.append(transaction)

        return transactions

    def choose_chain(self, chain):
        if not self.valid_chain(chain):
            return False

        if self.get_chain_work(chain) <= self.get_chain_work(self.chain):
            return False

        old_chain = self.chain

        transactions = self.restore_orphaned_transactions(
            old_chain,
            chain
        )

        self.chain = chain
        replace_blocks(chain)
        self.available_utxos = rebuild_utxos(chain)
        self.spent_utxos = []

        new_transaction_ids = {
            transaction.get('transaction_id')
            for block in chain
            for transaction in block['transactions']
        }

        self.current_transactions = []

        for transaction in transactions:
            transaction_id = transaction.get('transaction_id')

            if transaction_id in new_transaction_ids:
                continue

            validation_utxos = list(self.available_utxos)

            if not valid_transaction(
                transaction,
                validation_utxos,
                self.last_block['index'] + 1
            ):
                continue

            for utxo in transaction['inputs']:
                self.available_utxos.remove(utxo)
                self.spent_utxos.append(utxo)

            for index, output in enumerate(transaction['outputs']):
                self.available_utxos.append(
                    create_utxo(
                        transaction['transaction_id'],
                        index,
                        output['owner'],
                        output['amount']
                    )
                )

            self.current_transactions.append(transaction)

        replace_utxos(self.available_utxos)

        clear_mempool()

        for transaction in self.current_transactions:
            save_mempool_transaction(transaction)

        return True

    def valid_received_block(self, block):
        difficulty = get_difficulty(self.chain)

        if not valid_block(block):
            return False

        if block['previous_hash'] != hash(self.last_block):
            return False

        if not valid_proof(
            self.last_block['proof'],
            block['proof'],
            difficulty
        ):
            return False

        validation_utxos = list(self.available_utxos)

        if not self._valid_block_transactions(
            block,
            self.chain,
            validation_utxos
        ):
            return False
        
        if not valid_coinbase(
            block['transactions'][0],
            self.chain,
            block['index'],
            block['transactions']
        ):
            return False

        return True

    def proof_of_work(self, last_proof, difficulty):
        proof = 0

        while valid_proof(last_proof, proof, difficulty) is False:
            proof += 1

        return proof

    def mine_block(self, miner_address):
        last_block = self.last_block
        difficulty = get_difficulty(self.chain)
        proof = self.proof_of_work(last_block['proof'], difficulty)

        block_index = last_block['index'] + 1

        reward = get_block_reward(block_index)

        total_fees = sum(
            transaction.get('fee', 0)
            for transaction in self.current_transactions
            if transaction.get('type') != 'coinbase'
        )

        total_reward = reward + total_fees

        coinbase = create_coinbase_transaction(
            miner_address,
            total_reward,
            block_index
        )

        if not valid_coinbase(
            coinbase,
            self.chain,
            block_index,
            self.current_transactions
        ):
            return None

        self.current_transactions.append(coinbase)

        previous_hash = hash(last_block)

        return self.add_block(proof, previous_hash)

    def mempool_full(self):
        return len(self.current_transactions) >= MEMPOOL_LIMIT

    @property
    def last_block(self):
        return self.chain[-1]


Blockchain.register_node = register_node
Blockchain.resolve_conflicts = resolve_conflicts
