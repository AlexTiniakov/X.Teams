import xmlrpc.client
import sys
import cmd
from  block import Block
from blockchain import Blockchain
from transaction import CoinbaseTransaction
import pickle

server = xmlrpc.client.Server('http://localhost:8000')
PEER_NODES = []


def add_node(node_url):
    PEER_NODES.append(node_url)

def mine():
    trs = []
    f = open('address', 'r')
    addr = f.readline()
    blocks = server.get_blocks()
    #print(blocks)
    if len(blocks) == 0:
        blockch = Blockchain(addr)
        if blockch.g_block.mining(16):
            blocks.append(blockch.g_block)
            server.add_block(blocks)
    while True:
        blocks = server.get_blocks()
        print(blocks)
        trs = []
        trs.append(CoinbaseTransaction(addr).ser)
        new_trx = server.get_transactions()
        for i in new_trx:
            trs.append(i)
        block_to_mine = Block(blocks[-1]['hash_rez'], trs)
        print('Ok')
        if block_to_mine.mining(16):
            blocks.append(block_to_mine)
            server.add_block(blocks)
            #print(block_to_mine)


    '''
    f = open('chain/blockchain', 'a')
    try:
        blocks = f.readlines()
        print(blocks)
    except:
        print('KO')
    f.close()
    '''

if __name__ == "__main__":
    mine()
'''
f = open('address')
addr = f.readline()
print(addr)
BLOCKCHAIN = Blockchain(addr)
'''
'''
def get_blocks(self):
        blocks = []
        with open('chain/blocks.pk1', 'rb') as input:
            blocks.append(pickle.load(input))
        return blocks


    def add_block(self, block):
        with open('chain/blocks.pk1', 'wb') as output:
            pickle.dump(block, output, pickle.HIGHEST_PROTOCOL)
            '''