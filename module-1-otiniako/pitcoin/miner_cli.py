import xmlrpc.client
import sys
import cmd
import block
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
    trs.append(CoinbaseTransaction(addr).ser)
    trs.append(server.get_transactions())
    blocks = server.get_blocks()
    '''blocks = []
    try:
        input = open('chain/blocks.pk1', 'rb')
        blocks.append(pickle.load(input))
    except:
        print('KO')
    blocks = []
    try:
        with open('chain/blocks.pk1', 'rb') as input:
            blocks.append(pickle.load(input))
        #return blocks
    except:
        #return blocks
        print('ecxept')'''
    print(type(blocks))
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