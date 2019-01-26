# Server code

#import xmlrpclib
import xmlrpc.server as SimpleXMLRPCServer
import pending_pool

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

    def repeat(self, astr, times):
        return astr * times


#server = xmlrpclib.ServerProxy("http://localhost:8000", verbose=True)
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_instance(Pitcoin())
server.register_function(lambda astr: '_' + astr, '_string')
server.serve_forever()