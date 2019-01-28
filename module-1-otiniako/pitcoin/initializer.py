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
            return jsonify({'blocks': blocks}), 201
        return jsonify({'blocks': []}), 201

@node.route('/chain', methods=['POST'])
def add_block():
    blocks = request.get_json()['blocks']
    with open('chain/blocks.pk1', 'wb') as output:
        pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
    print('new block is added')
    return jsonify({'success': True}), 201

if __name__ == "__main__":
    node.run()