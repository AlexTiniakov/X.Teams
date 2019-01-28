import xmlrpc.client
import sys
import cmd
from  block import Block
from blockchain import Blockchain
from transaction import CoinbaseTransaction
import pickle
import requests
from flask import json
import wallet as w


class Miner(cmd.Cmd):
    
    PEER_NODES = []
    URL = 'http://127.0.0.1:5000'
    def do_change(self, url):
        self.URL = url
        print('New url is: ', self.URL, '!')

    def do_add(self, node_url):
        if len(node_url) > 0:
            self.PEER_NODES.append(node_url)
            print('node ' + node_url + ' added to peer nodes!')
        else:
            print('Usage: add_node node_url')

    def do_mine(self, line):
        trs = []
        f = open('minerkey', 'r')
        privkey_WIF = f.readline().rstrip('\n')
        privkey_hex = w.decode_hex(privkey_WIF)
        privkey_d = int(privkey_hex, 16)
        addr = w.addr_from_privkey(privkey_d, 0)
        blocks = requests.get(self.URL + '/chain')
        blocks = json.loads(blocks.text)['blocks']
        #mine genesis block
        if len(blocks) == 0:
            blockch = Blockchain()
            gen_block = blockch.genesis_block(addr)
            if gen_block.mining(16):
                blocks.append(gen_block)
                url  = self.URL + '/chain'
                payload = {"blocks": self.to_json(blocks)}
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)
                if json.loads(res.text)['success']:
                    print(gen_block.hash_rez)
        #if blockchain not empty
        else:
            trs = []
            trs.append(CoinbaseTransaction(addr).ser)
            new_trx = requests.get(self.URL + '/transaction/pendings')
            new_trx = json.loads(new_trx.text)['trxs']
            for i in new_trx:
                trs.append(i)
            block_to_mine = Block(blocks[-1]['hash_rez'], trs)
            if block_to_mine.mining(16):
                blocks.append(block_to_mine)
                url  = self.URL + '/chain'
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

    def find_new_chains(self):
        other_chains = []
        for node_url in self.PEER_NODES:
            blocks = requests.get(node_url + '/chain')
            blocks = json.loads(blocks.text)['blocks']
            if Blockchain().is_valid_chain(blocks):
                other_chains.append(blocks)
        return other_chains

    def find_trx_in_chain(self, trx, blocks):
        if trx[4:39] == '0'*35:
            return True
        for block in blocks:
            for trx_b in block['transactions']:
                if trx_b == trx:
                    return True
        return False

    def post_trx_back(self, blocks, longest_chain):
        for block in blocks:
            if block not in longest_chain:
                for trx in block['transactions']:
                    if self.find_trx_in_chain(trx, longest_chain) == False:
                        url     = self.URL + '/transaction/new'
                        payload = {"transaction": trx}
                        headers = {"Content-Type": "application/json"}
                        requests.post(url, json=payload, headers=headers)

    def do_consensus(self, line):
        other_chains = self.find_new_chains()
        blocks = requests.get(self.URL + '/chain')
        blocks = json.loads(blocks.text)['blocks']
        longest_chain = blocks
        for chain in other_chains:
            if len(longest_chain) < len(chain):
                longest_chain = chain
        if longest_chain == blocks:
            print('Consensus: your blockchain is the longest one!')
        else:
            self.post_trx_back(blocks, longest_chain)
            blocks = longest_chain
            url  = self.URL + '/chain'
            payload = {"blocks": self.to_json(blocks)}
            headers = {"Content-Type": "application/json"}
            requests.post(url, json=payload, headers=headers)
            print('Your node was upgrated!')


if __name__ == "__main__":
        Miner().cmdloop()