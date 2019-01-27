# Server code

#import xmlrpclib
import xmlrpc.server as SimpleXMLRPCServer
import pending_pool
import pickle
import os
import json
import time
import hashlib as hasher
import base64
import flask
from flask import Flask, request, json, jsonify
from multiprocessing import Process, Pipe
import ecdsa
from pending_pool import assept

node = Flask(__name__)
node.config['DEBUG'] = True

@node.route('/', methods=['GET', 'POST'])
def home():
    return 'Ok'

@node.route('/transaction/new', methods=['POST'])
def broadcast():
    #print(request.is_json)
    new_txion = request.get_json()['transaction']
    if assept(new_txion):
        return jsonify({'success': True}), 201
    else:
        return jsonify({'success': False}), 201

@node.route('/balance', methods=['POST'])
def get_balance():
        balance = 0
        addr = request.get_json()['addr']
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks = pickle.load(input)
            for blk in blocks:
                for transactions in blk['transactions']:
                    if addr in transactions:
                        #print(transactions)
                        if transactions.find(addr) < 20:
                            balance -= int(transactions[:4], 16)
                        elif transactions.find(addr) > 30:
                            balance += int(transactions[:4], 16)
        return jsonify({'balance': balance}), 201

@node.route('/transaction/pendings', methods=['GET'])
def get_transactions():
    trxs = pending_pool.get_from_mem()
    return jsonify({'trxs': trxs}), 201

@node.route('/chain', methods=['GET'])
def get_blocks():
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks = pickle.load(input)
                '''blocks_to_send_json = []
                for block in blocks:
                    block = {'timestamp': str(block), 
                    'previous_hash': block.previous_hash, 
                    'transactions': block.transactions, 
                    'm_root': block.m_root, 
                    'hash_rez': block.hash_rez, 
                    'nonce': str(block.nonce)}
                    blocks_to_send_json.append(block)'''
            return jsonify({'blocks': blocks}), 201
        return jsonify({'blocks': []}), 201

@node.route('/chain', methods=['POST'])
def add_block():
    blocks = request.get_json()['blocks']
    with open('chain/blocks.pk1', 'wb') as output:
        pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
    print('block is added')
    return jsonify({'success': True}), 201

class Pitcoin:
    

    def get_transactions(self):
        return pending_pool.get_from_mem()

    def get_blocks(self):
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks = pickle.load(input)
            return blocks
        return []
        

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