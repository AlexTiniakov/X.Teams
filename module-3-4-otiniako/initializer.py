import xmlrpc.server as SimpleXMLRPCServer
import pending_pool
import pickle
import os
import json
import time
import hashlib as hasher
import base64
import flask
from flask import Flask, request, json, jsonify, render_template
from multiprocessing import Process, Pipe
import ecdsa
from pending_pool import assept
from utxo_set import Utxo
from block import Block
import requests
import sys
import wallet as w
from blockchain import Blockchain
import hashlib
from serializer import Deserializer
import binascii
import base58

PEER_NODES = []
node = Flask(__name__)
node.config['DEBUG'] = True


@node.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@node.route('/search', methods=['GET'])
def search():
    to_search = request.args.get('info')
    height = -1
    transactions = []
    is_addr = 1
    try:
        height = int(to_search)
    except:
        print("not height")
    if height != -1:
        is_addr = 0
        port, host = get_url()
        url = "http://"+host+":"+port+"/block?height="+to_search
        payload = {"node_url": url}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        block = requests.get(url, json=payload, headers=headers)
        blc = block.json()['block']
        #print(blc)
        try:
            i = 0
            for tr in blc["transactions"]:
                blc["transactions"][i] = Deserializer(tr).trx
                i += 1
        except:
            pass
        return jsonify({"block": blc}), 201
        #return JSON.parse(block.responseText), 201
    else:
        port, host = get_url()
        url = "http://"+host+":"+port+"/chain"
        payload = {"node_url": url}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        blocks = requests.get(url, json=payload, headers=headers)
        #chain = blocks.text["blocks"]
        chain = blocks.json()
        for block in chain["blocks"]:
            #print(block["hash_rez"])
            if block["hash_rez"] == to_search:
                i = 0
                for tr in block["transactions"]:
                    block["transactions"][i] = Deserializer(tr).trx
                    i += 1
                return jsonify({"block": block}), 201
            # address?
            for trx in block["transactions"]:
                deser_trx = Deserializer(trx).trx
                #print(deser_trx)

                #address?
                if is_addr == 1:
                    for inp in deser_trx['inputs']:
                        #print(base58.b58encode_check(bytes.fromhex('00'+inp["pk_script"][6:-4])).decode('utf-8'))
                        try:
                            if inp['txouthash'] != '0'*64 and base58.b58encode_check(bytes.fromhex('00'+inp["pk_script"][6:-4])).decode('utf-8') == to_search:
                                if deser_trx not in transactions:
                                    transactions.append(deser_trx)
                        except:
                            is_addr = 0
                    for outs in deser_trx['outputs']:
                        try:
                            if base58.b58encode_check(bytes.fromhex('00'+outs["pk_script"][6:-4])).decode('utf-8') == to_search:
                                if deser_trx not in transactions:
                                    transactions.append(deser_trx)
                        except:
                            is_addr = 0
                    #print(transactions)
                    #print(is_addr)
                    #transactions = list(set(transactions))

                # transaction?
                if to_search == binascii.hexlify(hashlib.sha256(hashlib.sha256(bytes.fromhex(trx)).digest()).digest()).decode('utf-8'):
                    #return render_template('transaction.html', trx=Deserializer(trx).trx), 202
                    return jsonify({"transaction": Deserializer(trx).trx}), 202
    if is_addr == 1:
        port, host = get_url()
        utxo = requests.get("http://"+host+":"+port+"/utxo")
        utxo = utxo.json()
        balance = requests.get("http://"+host+":"+port+"/balance?addr="+to_search)
        unspend = []
        #print(utxo)
        for i in utxo:
            print(i)
            if i['adress'] == to_search:
                unspend.append(i)
        if len(transactions) > 0:
            return jsonify({'balance': balance.json()['balance'],'transactions': transactions, 'unspend outputs': unspend}), 203
    return jsonify({'to_search': to_search}), 200

@node.route('/node/new', methods=['POST'])
def do_add():
    PEER_NODES.append(request.get_json()['node_url'])
    print('node ' + PEER_NODES[-1] + ' added to peer nodes!')
    return jsonify({'success': True}), 201

@node.route('/transaction/new', methods=['POST'])
def broadcast():
    new_txion = request.get_json()['transaction']
    if assept(new_txion):
        return jsonify({'success': True}), 201
    else:
        return jsonify({'success': False}), 201

@node.route('/balance', methods=['GET'])
def get_balance():
    balance = -1
    addr = request.args.get('addr')
    if not addr:
        addr = request.get_json()['addr']
    if os.path.isfile('chain/utxo.pk1'):
        with open('chain/utxo.pk1', 'rb') as input:
            utxo = pickle.load(input)
            balance = utxo.get_balance(addr)
        return jsonify({'balance': balance}), 201
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


@node.route('/block/receive', methods=['POST'])
def receive_blocks():
    blocks = request.get_json()['blocks']
    #print(blocks[0])
    with open('chain/blocks.pk1', 'rb') as input:
        blocks_my = pickle.load(input)
    if len(blocks) > len(blocks_my):
        utxo = Utxo("")
        for block in blocks:
            for transaction in block["transactions"]:
                utxo.add_dell(transaction)
        #print(utxo.unspend_outputs)
        with open('chain/blocks.pk1', 'wb') as output:
            pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
        with open('chain/utxo.pk1', 'wb') as output:
            pickle.dump(utxo, output, pickle.HIGHEST_PROTOCOL)
        print('new block is added')
        for peer in PEER_NODES:
            try:
                url = peer + '/block/receive'
                payload = {"blocks": to_json(blocks)}
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)
            except:
                pass
        return jsonify({'success': True}), 201
    elif len(blocks) == len(blocks_my):
        return jsonify({'success': True}), 201
    else:
        return jsonify({'success': False}), 201

@node.route('/chain', methods=['POST'])
def add_block():
    blocks = request.get_json()['blocks']
    #print(blocks[0])
    for peer in PEER_NODES:
        url = peer + '/block/receive'
        payload = {"blocks": to_json(blocks)}
        headers = {"Content-Type": "application/json"}
        res = requests.post(url, json=payload, headers=headers)
        #fasle значит, что на этой ноде цепочка длиннее. Переключаемся на нее.
        if json.loads(res.text)['success'] == False:
            blocks = requests.get(peer + '/chain')
            blocks = json.loads(blocks.text)['blocks']
            print("Longer chain was found!")
    utxo = Utxo("")
    for block in blocks:
        for transaction in block["transactions"]:
            utxo.add_dell(transaction)
    #print(utxo.unspend_outputs)
    with open('chain/blocks.pk1', 'wb') as output:
        pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
    with open('chain/utxo.pk1', 'wb') as output:
        pickle.dump(utxo, output, pickle.HIGHEST_PROTOCOL)
    #print('new block is added')
    return jsonify({'success': True}), 201

@node.route('/chain/length', methods=['GET'])
def get_length():
    blocks = []
    with open('chain/blocks.pk1', 'rb') as input:
        blocks = pickle.load(input)
    return str(len(blocks))

@node.route('/block', methods=['GET'])
def get_heigth_block():
    blocks = []
    try:
        length = int(request.args.get('height'))
    except:
        return jsonify({'block': "invalid length"}), 201
    with open('chain/blocks.pk1', 'rb') as input:
        blocks = pickle.load(input)
    if length > len(blocks) - 1 or length < 0:
        return jsonify({'block': "invalid length"}), 201
    return jsonify({'block': blocks[length]}), 201

@node.route('/block/last', methods=['GET'])
def get_last_block():
    blocks = []
    with open('chain/blocks.pk1', 'rb') as input:
        blocks = pickle.load(input)
    return jsonify({'last_block': blocks[-1]}), 201

@node.route('/utxo', methods=['GET'])
def get_txid():
    with open('chain/utxo.pk1', 'rb') as input:
        utxo = pickle.load(input)
        if not request.get_json():
            return jsonify(utxo.unspend_outputs)
        prv_txid, tx_out_index, balance = utxo.get_prv_txid(request.get_json()['adress'])
    return jsonify({'prv_txid': prv_txid, 'tx_out_index': tx_out_index, 'balance': balance}), 201

@node.route('/getDifficulty', methods=['GET'])
def get_diff():
    complexity = 20
    target = 2**(256-complexity)
    if os.path.isfile('chain/blocks.pk1'):
        with open('chain/blocks.pk1', 'rb') as input:
            blocks = pickle.load(input)
        target = blocks[-1]['target']
        if len(blocks) % 50 == 0:
            
            #print("blocks[-1]['timestamp']: ", blocks[-1]['timestamp'])
            
            t = 0
            for i in range(1,50):
                t += float(blocks[-i]['timestamp']) - float(blocks[-i-1]['timestamp'])
            delta = t/49
            if delta < 30:
                target /= 1.15
            elif delta > 40:
                target *= 1.15
            target = int(target)
            print(target)
    if not request.get_json():
            return jsonify(target)
    return target

def to_json(blocks):
        blocks_to_send_json = []
        for block in blocks:
            if type(block)==Block:
                block = {'version': block.version,    
                'timestamp': str(block.timestamp), 
                'previous_block_hash': block.previous_hash, 
                'transactions': block.transactions, 
                'merkle_root': block.m_root, 
                'hash_rez': block.hash_rez, 
                'nonce': str(block.nonce),
                'hight': block.hight,
                'target': block.target,
                'suply': block.suply}
            elif type(block)==dict:
                #print(block)
                block = {'version': block['version'],
                'timestamp': block['timestamp'], 
                'previous_block_hash': block['previous_block_hash'], 
                'transactions': block['transactions'], 
                'merkle_root': block['merkle_root'], 
                'hash_rez': block['hash_rez'], 
                'nonce': block['nonce'],
                'hight': block['hight'],
                'target': block['target'],
                'suply': block['suply']}
            blocks_to_send_json.append(block)
        return blocks_to_send_json

def mine_gen_block():
    f = open('minerkey', 'r')
    blocks = []
    privkey_WIF = f.readline().rstrip('\n')
    privkey_hex = w.decode_hex(privkey_WIF)
    privkey_d = int(privkey_hex, 16)
    addr = w.addr_from_privkey(privkey_d, 0)
    blockch = Blockchain()
    gen_block = blockch.genesis_block(addr)
    if gen_block.mining(0):
        print(gen_block.hash_rez)
        blocks.append(gen_block)
        blocks = to_json(blocks)
        utxo = Utxo("")
        for block in blocks:
            for transaction in block["transactions"]:
                utxo.add_dell(transaction)
        #print(utxo.unspend_outputs)
        with open('chain/blocks.pk1', 'wb') as output:
            pickle.dump(blocks, output, pickle.HIGHEST_PROTOCOL)
        with open('chain/utxo.pk1', 'wb') as output:
            pickle.dump(utxo, output, pickle.HIGHEST_PROTOCOL)


def test():
    port = '5000'
    host = '127.0.0.1'
    try:
        f = open('url', 'r')
        line = f.readline().rstrip('\n')
        host = line.split(':')[0]
        print("Your host is: ", host)
        port = line[-4:]
        print("Your port is: ", port)
    except:
        print("Your host is: ", host)
        print("Your port is: ", port)
    node.run(port=port)

def get_url():
    port = '5000'
    host = '0.0.0.0'
    try:
        f = open('url', 'r')
        line = f.readline().rstrip('\n')
        host = line.split(':')[1][2:]
        print("Your host is: ", host)
        port = line[-4:]
        print("Your port is: ", port)
    except:
        print('Can\'t open file "url"!')
        print("Your host is: ", host)
        print("Your port is: ", port)
    return port, host

def flip_byte_order(string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped

if __name__ == "__main__":
    port, host = get_url()
    mine_gen_block()
    node.run(host=host, port=port, threaded=True)
