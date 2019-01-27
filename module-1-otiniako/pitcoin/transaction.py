import hashlib
import wallet as w
from serializer import Serializer

class Transaction(object):

    sig = ''
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

    def to_serialize(self):
        self.for_ser = []
        self.for_ser.append(self.amount)
        self.for_ser.append(self.sender)
        self.for_ser.append(self.recipient)
        self.for_ser.append(self.pubkey_sig)
        self.for_ser.append(self.sig)

class CoinbaseTransaction(Transaction):

    def __init__(self, recipient, amount=50):
        super().__init__('0'*35, recipient, amount)
        try:
            f = open('minerkey', 'r')
            pk = f.readline()
            pk_hex = w.decode_hex(pk)
            self.singin(pk_hex)
            self.ser = Serializer(self).ser

        except IOError:
            print("Error: can\'t find file or read data")
        

