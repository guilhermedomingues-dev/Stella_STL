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
    rebuild_utxos
)
from config import BLOCK_REWARD, MATURATION_BLOCKS
from core.transaction import create_coinbase_transaction, valid_transaction
from core.utxo import create_utxo
from network.node import Node
from network.consensus import register_node, resolve_conflicts


class Blockchain:
    def __init__(self):
        initialize_database()
        self.current_transactions = []
        self.chain = get_blocks()
        self.available_utxos = get_utxos()
        self.nodes = set()
        self.node = Node()
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

    def add_block(self, proof, previous_hash=None):
        valid_transactions = [
            transaction
            for transaction in self.current_transactions
            if transaction.get('type') == 'coinbase'
            or valid_transaction(
                transaction,
                self.available_utxos,
                self.last_block['index'] + 1
            )
        ]

        block = new_block(
            index=len(self.chain) + 1,
            transactions=valid_transactions,
            proof=proof,
            previous_hash=previous_hash
        )

        self.chain.append(block)
        save_block(block)
        self.process_matured_coinbases()
        self.node.broadcast_block(block)

        return block

    def receive_block(self, block):
        self.chain.append(block)
        save_block(block)
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

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        difficulty = get_difficulty(chain[:current_index])

        while current_index < len(chain):
            block = chain[current_index]

            if not valid_block(block):
                return False

            if block['previous_hash'] != hash(last_block):
                return False

            if not valid_proof(last_block['proof'], block['proof'], difficulty):
                return False

            if not valid_coinbase(
                block['transactions'][0],
                chain[:current_index],
                block['transactions']
            ):
                return False

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

        for block in old_chain:
            for transaction in block['transactions']:
                if transaction.get('type') == 'coinbase':
                    continue

                transaction_id = transaction.get('transaction_id')

                if transaction_id in new_transaction_ids:
                    continue

                if valid_transaction(
                    transaction,
                    self.available_utxos,
                    self.last_block['index'] + 1
                ):
                    self.current_transactions.append(transaction)

    def choose_chain(self, chain):
        if not self.valid_chain(chain):
            return False

        if self.get_chain_work(chain) <= self.get_chain_work(self.chain):
            return False

        old_chain = self.chain

        self.restore_orphaned_transactions(old_chain, chain)

        self.chain = chain
        self.available_utxos = rebuild_utxos(chain)

        return True

    def valid_received_block(self, block):
        difficulty = get_difficulty(self.chain)

        if not valid_block(block):
            return False

        if block['previous_hash'] != hash(self.last_block):
            return False

        if not valid_proof(self.last_block['proof'], block['proof'], difficulty):
            return False

        if not valid_coinbase(
            block['transactions'][0],
            self.chain,
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