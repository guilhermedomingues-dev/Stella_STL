"""
Classe responsável por gerenciar a blockchain e sua cadeia de blocos.
"""

from core.block import new_block, hash, valid_block
from core.mining import valid_coinbase, valid_proof
from persistence.database import initialize_database, get_blocks, save_block, get_utxos
from config import BLOCK_REWARD
from core.transaction import create_coinbase_transaction

class Blockchain:
    def __init__(self):
        initialize_database()
        self.current_transactions = []
        self.chain = get_blocks()
        self.available_utxos = get_utxos()
        self.nodes = set()

        if not self.chain:
            self.chain.append(new_block(index=1, transactions=[], proof=100, previous_hash=1))
            save_block(self.chain[0])

    def add_block(self, proof, previous_hash=None):
        block = new_block(
            index=len(self.chain) + 1,
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash
        )
        self.current_transactions = []
        self.chain.append(block)
        save_block(block)
        return block

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if not valid_block(block):
                return False

            if block['previous_hash'] != hash(last_block):
                return False

            if not valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def choose_chain(self, chain):
        if len(chain) <= len(self.chain):
            return False

        if not self.valid_chain(chain):
            return False

        self.chain = chain
        return True

    def valid_received_block(self, block):
        if not valid_block(block):
            return False

        if block['previous_hash'] != hash(self.last_block):
            return False

        if not valid_proof(self.last_block['proof'], block['proof']):
            return False

        return True

    def proof_of_work(self, last_proof):
        proof = 0

        while valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def mine_block(self, miner_address):
        last_block = self.last_block
        proof = self.proof_of_work(last_block['proof'])

        coinbase = create_coinbase_transaction(
            miner_address,
            BLOCK_REWARD
        )

        if not valid_coinbase(coinbase, self.chain):
            return None        

        self.current_transactions.append(coinbase)

        previous_hash = hash(last_block)

        return self.add_block(proof, previous_hash)

    @property
    def last_block(self):
        return self.chain[-1]