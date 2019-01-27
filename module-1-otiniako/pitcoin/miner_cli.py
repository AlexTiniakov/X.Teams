import xmlrpc.client
import sys
import cmd
from  block import Block
from blockchain import Blockchain
from transaction import CoinbaseTransaction
import pickle
import requests
from flask import json


class Miner(cmd.Cmd):
    
    PEER_NODES = []
    def do_add_node(self, node_url):
        PEER_NODES.append(node_url)

    def do_mine(self, line):
        trs = []
        f = open('address', 'r')
        addr = f.readline()
        blocks = requests.get('http://127.0.0.1:5000/chain')
        blocks = json.loads(blocks.text)['blocks']
        print(blocks)
        if len(blocks) == 0:
            blockch = Blockchain(addr)
            if blockch.g_block.mining(16):
                blocks.append(blockch.g_block)
                url  = 'http://127.0.0.1:5000/chain'
                payload = {"blocks": self.to_json(blocks)}
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)
                if json.loads(res.text)['success']:
                    print(blockch.g_block.hash_rez)
        else:
            trs = []
            trs.append(CoinbaseTransaction(addr).ser)
            new_trx = requests.get('http://127.0.0.1:5000/transaction/pendings')
            new_trx = json.loads(new_trx.text)['trxs']
            for i in new_trx:
                trs.append(i)
            block_to_mine = Block(blocks[-1]['hash_rez'], trs)
            if block_to_mine.mining(16):
                blocks.append(block_to_mine)
                url  = 'http://127.0.0.1:5000/chain'
                payload = {"blocks": self.to_json(blocks)}
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)
                if json.loads(res.text)['success']:
                    print(block_to_mine.hash_rez)

    def to_json(self, blocks):
        blocks_to_send_json = []
        for block in blocks:
            if type(block)==Block:
                block = {'timestamp': str(block.timestamp), 
                'previous_hash': block.previous_hash, 
                'transactions': block.transactions, 
                'm_root': block.m_root, 
                'hash_rez': block.hash_rez, 
                'nonce': str(block.nonce)}
            elif type(block)==dict:
                block = {'timestamp': block['timestamp'], 
                'previous_hash': block['previous_hash'], 
                'transactions': block['transactions'], 
                'm_root': block['m_root'], 
                'hash_rez': block['hash_rez'], 
                'nonce': block['nonce']}
            blocks_to_send_json.append(block)
        return blocks_to_send_json
'''
    def do_find_new_chains():
        other_chains = []
        for node_url in self.PEER_NODES:
            blocks = requests.get(node_url + '/chain').content
            blocks = json.loads(blocks)
            if Blockchain().is_valid_chain(blocks):
                other_chains.append(blocks)
        return other_chains

    def do_consensus():
        other_chains = find_new_chains()
        blocks = server.get_blocks()
        longest_chain = blocks
        for chain in other_chains:
            if len(longest_chain) < len(vhain):
                longest_chain = chain
        if longest_chain == blocks:
            return False
        else:
            blocks = longest_chain
            return blocks
        
        f = open('chain/blockchain', 'a')
        try:
            blocks = f.readlines()
            print(blocks)
        except:
            print('KO')
        f.close()
'''

if __name__ == "__main__":
        Miner().cmdloop()