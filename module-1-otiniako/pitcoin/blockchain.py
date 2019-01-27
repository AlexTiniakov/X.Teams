from block import Block
import pending_pool
from transaction import Transaction, CoinbaseTransaction
from serializer import Serializer

class Blockchain(object):

    def __init__(self, addr):
        self.info = []
        self.complexity = 2*8
        try:
            f = open('chain/blocks', 'r')
            self.BLOCKCHAIN = f.readlines()
            #print(self.BLOCKCHAIN)
            f.close()
        except:
            f = open('chain/blocks', 'a')
            self.block_to_mine = self.genesis_block(addr)
            print(self.block_to_mine.transactions)
        self.g_block = self.genesis_block(addr)

    def mine(self, block):
        '''
        calls the mining method on the Block instance with passing the
        complexity parameter. At the class level, determine the value 2
        (the number of zeros at the beginning of the hash)
        '''
        #self.block.mining(self.complexity)
        return

    def resolve_conflicts(self, blocks_my, blocks_other):
        '''
        resolve conflicts between blockchain's nodes by replacing
        our chain with the longest one in the network. We're only looking
        for chains longer than ours. Grab and verify the chains from all
        the nodes in our network. Where does the node request comes we will
        review later when implementing Network issues and interfaces
        '''
        return

    def is_valid_chain(self, blocks):
        '''
        loops over all the blocks in the chain and verify if they are properly
        linked together and nobody has tampered with the hashes. By checking
        the blocks it also verifies the (signed) transactions inside of them by
        recalculating merkle root with merkle.py helper. You can make
        block_validator.py helper, it’s up to you
        '''
        return

    def add_node(self, url):
        '''
        add a new node to the list of nodes, accepts an URL without scheme
        like ‘192.168.0.2:5000'
        '''
        return url

    def genesis_block(self, addr):
        '''
        creates a genesis block in the chain, initializing the class
        Block with only one CoinbaseTrascation and the zero value of the previous hash
        '''
        transactions = CoinbaseTransaction(addr, 50).ser
        return Block('0'*64, [transactions,])

    def submit_tx(self):
        '''
        web api route for receiving transaction and push it to pending pool. The route is
        /transaction/new
        '''
        try:
            f = open('transaction/new', 'r')
        except IOError:
            return
        mem = f.readlines()
        f.close()
        f = open('transaction/pending', 'a')
        mem.split()
        for i in mem:
            return pending_pool.accept(i)