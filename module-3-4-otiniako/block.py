from merkle import merkle_root
import hashlib
from tx_validator import validate
import time
import pickle
import requests
from utxo_set import Utxo
import os

class Block(object):
    
    def __init__(self, previous_hash, transactions, last_length, target=2**(256-20)):
        if os.path.isfile('chain/utxo.pk1'):
            with open('chain/utxo.pk1', 'rb') as input:
                utxo = pickle.load(input)
            self.suply = utxo.get_suply()
        else:
            self.suply = 0
        self.version = '16000000'
        self.target = target
        self.hight = last_length + 1
        self.timestamp = str(time.time())
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.m_root = merkle_root(self.transactions.copy())[0]

    def validate_tx(self):
        for i in self.transactions:
            if validate(i)==False:
                return False
        return True

    def mining(self, hight):
        try:
            f = open('url', 'r')
            URL = f.readline().rstrip('\n')
        except:
            URL = 'http://127.0.0.1:5000'
        trx_ser = ''
        header = self.version + self.previous_hash + self.m_root + self.flip_byte_order(self.timestamp) + hex(self.target)[2:]
        max_nonce = 2**32
        t = time.time()
        for nonse in range(max_nonce):
            if time.time() - t > 5:
                t = time.time()
                if hight > 0 and hight < int(requests.get(URL + '/chain/length').text):
                    return False
            hash_rezult = hashlib.sha256(header.encode('utf-8') + str(nonse).encode('utf-8')).hexdigest()
            if int(hash_rezult, 16) < self.target:
                self.hash_rez = hash_rezult
                self.nonce = nonse
                if hight > 0 and hight < int(requests.get(URL + '/chain/length').text):
                    return False
                return True
        return False

    def flip_byte_order(self, string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped