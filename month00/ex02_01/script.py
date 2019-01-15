from slickrpc import Proxy
from bitcoinrpc.config import read_default_config

cfg = read_default_config(None)
user=cfg['rpcuser']
password=cfg['rpcpassword']

bitcoin = Proxy("http://%s:%s@localhost:18332"%(user, password))
print(bitcoin.getbalance())
