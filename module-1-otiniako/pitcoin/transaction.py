import hashlib
import wallet as w

class Transaction(object):

    sig = b''
    pubkey_sig = ''
    ser = ''

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount =  hex(int(amount))[2:]
        self.hash256 = self.hash()

    def hash(self):
        to_hash = self.sender + self.recipient + self.amount
        return hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

    def singin(self, privkey):
        self.sig, self.pubkey_sig = w.sign_message(privkey, self.hash256)

class CoinbaseTransaction(Transaction):

    def __init__(self, recipient, amount=50):
        super().__init__('0'*64, recipient, amount)
        try:
            f = open('minerkey', 'r')
        except IOError:
            print("Error: can\'t find file or read data")
        pk = f.readline()
        pk_hex = w.decode_hex(pk)
        self.singin(pk_hex)

