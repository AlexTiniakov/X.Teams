# Server code

#import xmlrpclib
import xmlrpc.server as SimpleXMLRPCServer
import pending_pool
import pickle
import os

class Pitcoin:

    def broadcast(self, transaction):
        try:
            string = pending_pool.assept(transaction)
            return string
        except IndexError:
            return 'Usage: broadcast <serialized transaction>'
        return pending_pool.assept(transaction)

    def get_transactions(self):
        return pending_pool.get_from_mem()

    def get_blocks(self):
        blocks = []
        if os.path.isfile('chain/blocks.pk1'):
            with open('chain/blocks.pk1', 'rb') as input:
                blocks.append(pickle.load(input))
        return blocks
        

    def add_block(self, block):
        with open('chain/blocks.pk1', 'wb') as output:
            pickle.dump(block, output, pickle.HIGHEST_PROTOCOL)
        print('block is added')
'''
    def get_blocks(self):
        f = open('chain/blockchain', 'a')
        blocks = f.readlines()
        f.close()
        return blocks

    def check_block(self, block):
        return True

    def add_block(self, block):
        f = open('chain/blockchain', 'a')
        if self.check_block(block):
            f.write(block)
        f.close()
        '''


#server = xmlrpclib.ServerProxy("http://localhost:8000", verbose=True)
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_instance(Pitcoin())
server.serve_forever()