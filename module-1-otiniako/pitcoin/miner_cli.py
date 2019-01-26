import xmlrpc.client
import sys
import cmd
import block
from blockchain import Blockchain
from transaction import CoinbaseTransaction

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

if __name__ == "__main__":
    mine()
'''
f = open('address')
addr = f.readline()
print(addr)
BLOCKCHAIN = Blockchain(addr)
'''