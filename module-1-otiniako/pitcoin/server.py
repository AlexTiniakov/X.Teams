# Server code

#import xmlrpclib
import xmlrpc.server as SimpleXMLRPCServer
import pending_pool
import pickle
import os
import json
import requests
from flask import Flask, request

import time
import hashlib as hasher
import json
import requests
import base64
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
import ecdsa

node = Flask(__name__)
node.config['DEBUG'] = True

@node.route('/transaction/new', methods=['POST'])
def broadcast(self):
    print('ok')
    new_txion = request.get_json()
    print(new_txion)

class Pitcoin:
    '''
        def broadcast(self, transaction):
            try:
                string = pending_pool.assept(transaction)
                return string
            except IndexError:
                return 'Usage: broadcast <serialized transaction>'
    '''    
    

    def get_transactions(self):
        return pending_pool.get_from_mem()

    def get_blocks(self):
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks = pickle.load(input)
            return blocks
        return []
        
    def get_balance(self, addr):
        balance = 0
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks = pickle.load(input)
            for blk in blocks:
                for transactions in blk['transactions']:
                    if addr in transactions:
                        print(transactions)
                        if transactions.find(addr) < 20:
                            balance -= int(transactions[:4], 16)
                        elif transactions.find(addr) > 30:
                            balance += int(transactions[:4], 16)
        return balance

    def add_block(self, blocks):
        with open('chain/blocks.pk1', 'wb') as output:
            pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
        print('block is added')
'''
    def get_blocks(self):
        f = open('chain/blockchain', 'a')
        blocks = f.readlines()
        f.close()
        return blocks

    def check_block(self, block):
        return True

    def add_block(self, block):
        f = open('chain/blockchain', 'a')
        if self.check_block(block):
            f.write(block)
        f.close()
        '''

if __name__ == "__main__":
#server = xmlrpclib.ServerProxy("http://localhost:8000", verbose=True)
#server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
#server.register_instance(Pitcoin())
    node.run()
#server.serve_forever()