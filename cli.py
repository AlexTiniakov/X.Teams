# Client code

import xmlrpclib

server = xmlrpclib.Server('http://localhost:8000')
#server = xmlrpc.client.ServerProxy('http://localhost:8000')
print server.chop_in_half('sdf')
print server.repeat('Repetition is the key to learning!\n', 5)
print server._string('<= underscore')
#print server.python_string.join(['I', 'like it!'], " don't ")
#print server._privateFunction() # Will throw an exception
