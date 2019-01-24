from block import Block

from transaction import Transaction, CoinbaseTransaction
from serializer import Serializer

class Blockchain(object):
    
    def __init__(self, block):
        self.info = []
        self.complexity = 2*8
        self.block = block
    
    def mine(self):
        '''
        calls the mining method on the Block instance with passing the
        complexity parameter. At the class level, determine the value 2
        (the number of zeros at the beginning of the hash)
        '''
        self.block.mining(self.complexity)

    def resolve_conflicts(self):
        '''
        resolve conflicts between blockchain's nodes by replacing
        our chain with the longest one in the network. We're only looking
        for chains longer than ours. Grab and verify the chains from all
        the nodes in our network. Where does the node request comes we will
        review later when implementing Network issues and interfaces
        '''
        return

    def is_valid_chain(self):
        '''
        loops over all the blocks in the chain and verify if they are properly
        linked together and nobody has tampered with the hashes. By checking
        the blocks it also verifies the (signed) transactions inside of them by
        recalculating merkle root with merkle.py helper. You can make
        block_validator.py helper, it’s up to you
        '''

    def add_node(self):
        '''
        add a new node to the list of nodes, accepts an URL without scheme
        like ‘192.168.0.2:5000'
        '''

    def genesis_block(self, addr):
        '''
        creates a genesis block in the chain, initializing the class
        Block with only one CoinbaseTrascation and the zero value of the previous hash
        '''
        transactions = CoinbaseTransaction(addr, 50)
        self.g_block = Block('0'*64, transactions)
        self.mine()

    def submit_tx(self):
        '''
        web api route for receiving transaction and push it to pending pool. The route is
        /transaction/new
        '''