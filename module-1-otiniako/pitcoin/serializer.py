class Serializer(object):

    def __init__(self, tr):
        self.ser = self.add_zero(tr.amount, 4)
        self.ser += self.add_zero(tr.sender, 35)
        self.ser += self.add_zero(tr.recipient, 35)
        self.ser += tr.pubkey_sig
        self.ser += str(tr.sig)
    
    def add_zero(self, buf, nb):
        while len(buf) < nb:
            buf = '0' + buf
        return buf

class Deserializer(object):

    def del_zero(self, buf):
        while len(buf) > 0 and buf[0]=='0':
            buf = buf[1:]
        return buf

    def __init__(self, ser):
        trx = []
        trx.append(self.del_zero(ser[0:4]))
        if ser[4:39] == '0'*35:
            trx.append(ser[4:39])
        else:
            trx.append(self.del_zero(ser[4:39]))
        trx.append(self.del_zero(ser[39:74]))
        trx.append(ser[74:202])
        trx.append(ser[202:])
        self.trx = trx