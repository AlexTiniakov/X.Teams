from merkle import merkle_root
import hashlib
from tx_validator import validate
import time

_complexity = 25

class Block(object):
    def __init__(self, previous_hash, transactions):
        self.timestamp = time.time()
        self.nonse = 0
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.m_root = merkle_root(self.transactions)
        self.trx_ser = ''
        for i in self.transactions:
            self.trx_ser += i
        self.header = self.previous_hash + self.m_root + self.timestamp +\
        self.transactions
        self.hash, self.nonce = mining(self, _complexity)

    def validate_tx(self):
        for i in self.transactions:
            if validate(i)==False:
                return False
        return True

    def mining(self, complexity):
        max_nonce = 2**32
        nonce = 0
        target = 2**(256-complexity)
        for nonse in range(max_nonce):
            hash_rezult = hashlib.sha256(self.header.encode('utf-8') + str(nonce)).hexdigest()
            if long(hash_rezult, 16) < target:
                self.hash = hash_rezult
                self.nonce = nonce
                return True
        return False

    def hash_of_block(self):
        self.header += str(hex(self.nonse)[2:]
        self.hash = hashlib.sha256(self.header.encode('utf-8')).hexdigest()
