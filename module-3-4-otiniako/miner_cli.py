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

URL = 'http://127.0.0.1:5000'

class Miner(cmd.Cmd):
    
    PEER_NODES = []

    def do_change(self, url):
        URL = url
        print('New url is: ', URL, '!')

    def do_add(self, node_url):
        if len(node_url) > 0:
            self.PEER_NODES.append(node_url)
            try:
                url  = URL + '/node/new'
                payload = {"node_url": node_url}
                headers = {"Content-Type": "application/json"}
                requests.post(url, json=payload, headers=headers)
            except:
                pass
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
        try:
            blocks = requests.get(URL + '/chain')
        except:
            return
        blocks = json.loads(blocks.text)['blocks']
        if len(blocks) != 0:
            trs = []
            amount = 50*10**8/(2**int((len(blocks))/50))
            #print("amount: ", amount)
            trs.append(CoinbaseTransaction(addr, int(amount)).raw_tx_string)
            try:
                new_trx = requests.get(URL + '/transaction/pendings')
            except:
                return
            new_trx = json.loads(new_trx.text)['trxs']
            for i in new_trx:
                trs.append(i)
            target = requests.get(URL + '/getDifficulty')
            #print(target.text)
            block_to_mine = Block(blocks[-1]['hash_rez'], trs, len(blocks)-1, int(target.text))
            
            #complexity = json.loads(compl.text)["complexity"]
            if block_to_mine.mining(int(requests.get(URL + '/chain/length').text)):
                try:
                    blocks.append(block_to_mine)
                    url  = URL + '/chain'
                    payload = {"blocks": self.to_json(blocks)}
                    headers = {"Content-Type": "application/json"}
                    res = requests.post(url, json=payload, headers=headers)
                    if json.loads(res.text)['success']:
                        print('new block is added')
                        print(block_to_mine.hash_rez)
                except:
                    pass
            else:
                print("New block was added before you. Let's try again....")
                

    def do_mine_inf(self, line):
        while True:
            try:
            #compl = requests.get(URL + '/getDifficulty')
            #print("target = ", int(compl.text))
                self.do_mine("")
            except KeyboardInterrupt:
                sys.exit()
            except:
                pass

    def to_json(self, blocks):
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
                        url     = URL + '/transaction/new'
                        payload = {"transaction": trx}
                        headers = {"Content-Type": "application/json"}
                        requests.post(url, json=payload, headers=headers)

    def do_consensus(self, line):
        other_chains = self.find_new_chains()
        blocks = requests.get(URL + '/chain')
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
            url  = URL + '/chain'
            payload = {"blocks": self.to_json(blocks)}
            headers = {"Content-Type": "application/json"}
            requests.post(url, json=payload, headers=headers)
            print('Your node was upgrated!')

    def do_attack(self, line):
        while True:
            trs = []
            f = open('minerkey', 'r')
            privkey_WIF = f.readline().rstrip('\n')
            privkey_hex = w.decode_hex(privkey_WIF)
            privkey_d = int(privkey_hex, 16)
            addr = w.addr_from_privkey(privkey_d, 0)
            blocks = requests.get(URL + '/chain')
            blocks = json.loads(blocks.text)['blocks']
            if len(blocks) != 0:
                trs = []
                amount = 50*10**8/(2**int((len(blocks))/50))*100
                #print("amount: ", amount)
                trs.append(CoinbaseTransaction(addr, int(amount)).raw_tx_string)
                new_trx = requests.get(URL + '/transaction/pendings')
                new_trx = json.loads(new_trx.text)['trxs']
                for i in new_trx:
                    trs.append(i)
                target = requests.get(URL + '/getDifficulty')
                #print(target.text)
                block_to_mine = Block(blocks[-1]['hash_rez'], trs, len(blocks)-1, int(target.text))
                
                #complexity = json.loads(compl.text)["complexity"]
                if block_to_mine.mining(int(requests.get(URL + '/chain/length').text)):
                    blocks.append(block_to_mine)
                    url  = URL + '/chain'
                    payload = {"blocks": self.to_json(blocks)}
                    headers = {"Content-Type": "application/json"}
                    res = requests.post(url, json=payload, headers=headers)
                    if json.loads(res.text)['success']:
                        print('new block is added')
                        print(block_to_mine.hash_rez)
                else:
                    print("New block was added before you. Let's try again....")

if __name__ == "__main__":
    try:
        f = open('url', 'r')
        URL = f.readline().rstrip('\n')
        print("Your URL is: ", URL)
    except:
        print("Your URL is: ", URL)
    Miner().cmdloop()
