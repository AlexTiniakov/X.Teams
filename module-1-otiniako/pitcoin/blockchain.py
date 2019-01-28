from block import Block
import pending_pool
from transaction import Transaction, CoinbaseTransaction
from serializer import Serializer
from tx_validator import validate
from serializer import Deserializer

class Blockchain():

    def is_valid_chain(self, blocks):
        p_hash = '0'*64
        for block in blocks:
            if block['previous_hash'] != p_hash:
                return False
            p_hash = block['hash_rez']
            transactions = block['transactions']
            for trx in transactions:
                trx = Deserializer(trx).trx
                if validate(trx) == False:
                    return False
        return True

    def genesis_block(self, addr):
        transactions = CoinbaseTransaction(addr, 50).ser
        return Block('0'*64, [transactions,])