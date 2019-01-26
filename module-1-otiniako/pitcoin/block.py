from merkle import merkle_root
import hashlib
from tx_validator import validate
import time
import pickle




class Block(object):
    _complexity = 16
    
    def __init__(self, previous_hash, transactions):
        self.hash_r = ''
        self.timestamp = time.time()
        self.nonse = 0
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.m_root = merkle_root(self.transactions)
        print(self.m_root)
        self.trx_ser = ''
        for i in self.transactions:
            self.trx_ser += i
        self.header = self.previous_hash + self.m_root + self.timestamp +\
        self.trx_ser
        #mining(self, _complexity)
        #self.add_to_chain()

    def add_to_chain(self):
        #with open('company_data.pkl', 'wb') as output:
        return

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
            if int(hash_rezult, 16) < target:
                self.hash_r = hash_rezult
                self.nonce = nonse
                return True
        return False
'''
    def hash_of_block(self):
        self.header += str(hex(self.nonse)[2:]
        self.hash_r = hashlib.sha256(self.header.encode('utf-8')).hexdigest()
'''