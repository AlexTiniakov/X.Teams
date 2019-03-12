import struct
from utxo_set import Utxo
import hashlib
import binascii

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

    def flip_byte_order(self, string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped

    def __init__(self, ser):
        '''trx = []
        trx.append(self.del_zero(ser[0:4]))
        if ser[4:39] == '0'*35:
            trx.append(ser[4:39])
        else:
            trx.append(self.del_zero(ser[4:39]))
        trx.append(self.del_zero(ser[39:74]))
        trx.append(ser[74:202])
        trx.append(ser[202:])
        self.trx = trx'''

        self.trx = {}
        self.trx["hash"] = binascii.hexlify(hashlib.sha256(hashlib.sha256(bytes.fromhex(ser)).digest()).digest()).decode('utf-8')
        self.trx["version"] = int(self.flip_byte_order(ser[0:8]), 16)
        self.trx["inputs"] = []
        self.trx["nb_inputs"] = int(ser[8:10], 16)
        k = 10
        for i in range(self.trx["nb_inputs"]):
            begin_index = k
            end_index = begin_index + 32 * 2
            self.trx["inputs"].append({})
            buf = self.trx["inputs"][i]
            buf["txouthash"] = self.flip_byte_order(ser[begin_index:end_index])
            if buf["txouthash"] != "0"*64:
                buf["tx_out_index"] = ser[end_index:end_index+8]
                k = end_index + 8
                #print(ser[k:k+2], "  ", k)
                buf["len_sigskript"] = int(ser[k:k+2], 16) * 2 # потенциальный баг: если скрипт будет длинее 256?
                buf["len_signature"] = int(ser[k+2:k+4], 16) * 2 - 2
                k += 4
                buf["signature"] = ser[k:k+buf["len_signature"]]
                k = k+buf["len_signature"]
                #print("self.trx: ", self.trx)
                buf["sig_index"] = int(ser[k:k+2], 16) # всегда = 01
                buf["len_public_key"] = int(ser[k+2:k+4], 16)
                k += 4
                buf["public_key"] = ser[k:k+buf["len_public_key"]]
                buf["siquence"] = ser[k+buf["len_public_key"]:k+buf["len_public_key"]+8]
                k = k+buf["len_public_key"]+8
            else:
                buf["siquence"] = ser[end_index:end_index+8]
                buf["nb_coinbase"] = int(ser[end_index+8:end_index+8+2], 16) * 2
                buf["coinbase"] = ser[end_index+8+2:end_index+8+2+buf["nb_coinbase"]]
                k = end_index+18+buf["nb_coinbase"]
        self.trx["nb_outputs"] = int(ser[k:k+2], 16)
        k = k+2
        self.trx["outputs"] = []
        for i in range(self.trx["nb_outputs"]):
            self.trx["outputs"].append({})
            buf = self.trx["outputs"][i]
            buf["value"] = int(self.flip_byte_order(ser[k:k+16]), 16)
            buf["pk_script_bytes"] = int(ser[k+16:k+18], 16) * 2
            buf["pk_script"] = ser[k+18:k+18+buf["pk_script_bytes"]]
            #print(buf["pk_script"])
            k = k+18+buf["pk_script_bytes"]
        self.trx["locktime"] = ser[k:k+8]
        #print(k)
        #print(self.trx)
        #Utxo([trx,])
        
if __name__ == "__main__":
    Deserializer("01000000021a26798aee78e1e18458c085d4b6ec0750bc45ed0bc18f6aa971282fce45f10d000000006b483045022100f05bfee5a494e7790587a29cb4fe1363e712459a3336ef1b72be622b2212f5a3022051fcdde63c026c531bca9156b3a7eeb0744e27b573446c2620de637f595d83a7014203b79bf7efa319c04421f49cbcec43300d0d9d6d40616b5d0f3344aa8a832f994affffffffa4dbde2180135cef4e740674f0140ab957301a770464bb42bee896938b69fefa000000006a4730440220131dbac152a27f64ddec35ac94cdfe85abe8dfe196d1d108ff4ff44fc8886dd602204309c4ea57fc1edef9f7b04a9d568d6b499c638348dc6b718ea20eb424483c33014203b79bf7efa319c04421f49cbcec43300d0d9d6d40616b5d0f3344aa8a832f994affffffff0200f2052a010000001a76a9140025b4a9a820ae2a32716caf686dd50cad91579c5c88ac18ee052a010000001a76a9140025b4a9a820ae2a32716caf686dd50cad91579c5c88ac00000000")