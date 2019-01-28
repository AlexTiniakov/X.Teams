from merkle import merkle_root
import hashlib
from tx_validator import validate
import time
import pickle

class Block(object):
    _complexity = 16
    
    def __init__(self, previous_hash, transactions):
        self.timestamp = str(time.time())
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.m_root = merkle_root(self.transactions.copy())[0]

    def validate_tx(self):
        for i in self.transactions:
            if validate(i)==False:
                return False
        return True

    def mining(self, complexity):
        trx_ser = ''
        for i in self.transactions:
            trx_ser += i
        header = self.previous_hash + self.m_root + self.timestamp + trx_ser
        max_nonce = 2**32
        target = 2**(256-complexity)
        for nonse in range(max_nonce):
            hash_rezult = hashlib.sha256(header.encode('utf-8') + str(nonse).encode('utf-8')).hexdigest()
            if int(hash_rezult, 16) < target:
                self.hash_rez = hash_rezult
                self.nonce = nonse
                return True
        return False