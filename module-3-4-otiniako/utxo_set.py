import hashlib
import binascii
import base58
import wallet as wallet
class Utxo(object):

    def __init__(self, transactions):
        self.unspend_outputs = []
        for transaction in transactions:
            self.add_dell(transaction)
        #print(self.unspend_outputs)
    
    def add_dell(self, transaction):
        transaction = Deserializer(transaction)
        self.add_trx(transaction.trx)
        self.del_trx(transaction.trx)
    
    def add_trx(self, transaction):
        j = 0
        for out in transaction["outputs"]:
            self.unspend_outputs.append({})
            self.unspend_outputs[-1]["txouthash"] = transaction["hash"]
            self.unspend_outputs[-1]["tx_out_index"] = j
            self.unspend_outputs[-1]["value"] = transaction["outputs"][j]["value"]
            #self.unspend_outputs[-1]["adress"] = base58.b58encode_check(bytes.fromhex("80"+transaction["outputs"][j]["pk_script"][6:-4])).decode('utf-8')
            self.unspend_outputs[-1]["adress"] = self.get_addr(out)
            j += 1

    def get_addr(self, output):
        addr_string = output["pk_script"][6:-4]
        #print("addr_string: ", addr_string)
        addr_bytes = bytes.fromhex('00'+addr_string)
        return base58.b58encode_check(addr_bytes).decode('utf-8')

    def del_trx(self, transaction):
        i = 0
        to_del = []
        for inp in transaction["inputs"]:
            for unspend_outputs in self.unspend_outputs:
                #print(inp, " --- ", unspend_outputs)
                if inp["txouthash"] == unspend_outputs["txouthash"] and \
                    int(inp["tx_out_index"], 16) == unspend_outputs["tx_out_index"]:
                    to_del.append(unspend_outputs)
        for delete in to_del:
            self.unspend_outputs.remove(delete)

    def get_balance(self, addr):
        balance = 0
        for outs in self.unspend_outputs:
            if addr == outs["adress"]:
                balance += outs["value"]
                #print(balance)
        return balance

    def get_suply(self):
        suply = 0
        for outs in self.unspend_outputs:
            suply += outs["value"]
        return suply / (10**8)

    def get_prv_txid(self, adress):
        prv_txid = []
        tx_out_index = []
        balance = []
        for i in self.unspend_outputs:
            if i["adress"] == adress:
                #print(i)
                prv_txid.append(i["txouthash"])
                tx_out_index.append(i["tx_out_index"])
                balance.append(i["value"])
                #print(prv_txid, tx_out_index, balance)
        return prv_txid, tx_out_index, balance

class Deserializer(object):

    def del_zero(self, buf):
        while len(buf) > 0 and buf[0]=='0':
            buf = buf[1:]
        return buf

    def flip_byte_order(self, string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped

    def __init__(self, ser):
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
        #print("trx from UTXO: ", self.trx)
        #Utxo([trx,])
