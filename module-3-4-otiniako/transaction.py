import hashlib
import wallet as w
from wallet import decode_58, encode_58
from serializer import Serializer, Deserializer
from tx_validator import validate
import struct
import base58
import ecdsa
import binascii
import os
import requests
import json
from ecdsa.curves import SECP256k1


fee = 0
CURVE_ORDER = SECP256k1.order

class raw_tx:
            version 	= struct.pack("<L", 1)
            tx_in_count = struct.pack("<B", 1)
            tx_ins	= [] #TEMP
            tx_in_ser =  bytes.fromhex("")
            tx_out_count = struct.pack("<B", 1)
            tx_outs	= [] #TEMP
            tx_out_ser =  bytes.fromhex("")
            lock_time   = struct.pack("<L", 0)

class raw_tx_index:
            version 	= struct.pack("<L", 1)
            tx_in_count = struct.pack("<B", 1)
            tx_ins	= [] #TEMP
            tx_in_ser =  bytes.fromhex("")
            tx_out_count = struct.pack("<B", 1)
            tx_outs	= [] #TEMP
            tx_out_ser =  bytes.fromhex("")
            lock_time   = struct.pack("<L", 0)

class Transaction(object):

    def __init__(self, sender, recipients, amounts, privkey, prv_txid='0', tx_out_index=0):
        self.rtx = raw_tx()

        #prv_txid = self.get_prv_txid(sender, recipients, amounts, prv_txid)
        prv_txid, tx_out_index = self.get_prv_txid(sender, recipients, amounts, prv_txid, tx_out_index)
        self.prv_txid = prv_txid
        self.tx_out_index = tx_out_index
        #print(recipients)
        #sender_hashed_pubkey = binascii.hexlify(base58.b58decode_check(sender)).decode('utf-8')
        sender_hashed_pubkey = decode_58(sender)[2:]
        #print(sender_hashed_pubkey)
        self.sender_hashed_pubkey = sender_hashed_pubkey
        self.recipients = recipients
        self.amounts = amounts

        i = 0
        for prv_tx in prv_txid:
            self.rtx.tx_ins.append({})
            self.rtx.tx_ins[i]["txouthash"] = bytes.fromhex(self.flip_byte_order(prv_tx))
            self.rtx.tx_ins[i]["tx_out_index"] = struct.pack("<L",  tx_out_index[i]) # which nb of input we want to spend
            self.rtx.tx_ins[i]["script"] = bytes.fromhex("76a914%s88ac" % sender_hashed_pubkey) #OP_DUP (76) OP_HASH160 (a9) len of next var (20 == 0x14) OP_EQUALVERIFY (88) OP_CHECKSIG (ac)
            self.rtx.tx_ins[i]["script_bytes"] = struct.pack("<B", len(self.rtx.tx_ins[i]["script"]))
            #print(len(self.rtx.tx_ins[i]["script"]))
            self.rtx.tx_ins[i]["sequence"] = bytes.fromhex("ffffffff")
            self.rtx.tx_in_ser = ( self.rtx.tx_in_ser
                + self.rtx.tx_ins[i]["txouthash"]
                + self.rtx.tx_ins[i]["tx_out_index"]
                + self.rtx.tx_ins[i]["script_bytes"]
                + self.rtx.tx_ins[i]["script"]
                + self.rtx.tx_ins[i]["sequence"] )
            i += 1
        self.rtx.tx_in_count = struct.pack("<B", i)
        
        i = 0
        for recipient in recipients:
            #print("recipient: ", recipient)
            self.rtx.tx_outs.append({})
            recipient_hashed_pubkey = binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')[2:]
            self.rtx.tx_outs[i]["value"] = struct.pack("<Q", amounts[i]) #amount to send in output1
            self.rtx.tx_outs[i]["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
            self.rtx.tx_outs[i]["pk_script_bytes"] =  struct.pack("<B", len(self.rtx.tx_outs[i]["pk_script"]))
            self.rtx.tx_out_ser = ( self.rtx.tx_out_ser
                + self.rtx.tx_outs[i]["value"]
                + self.rtx.tx_outs[i]["pk_script_bytes"]
                + self.rtx.tx_outs[i]["pk_script"])
            i += 1
        self.rtx.tx_out_count = struct.pack("<B", i)

        self.raw_tx_string = (

            self.rtx.version
            + self.rtx.tx_in_count
            + self.rtx.tx_in_ser
            + self.rtx.tx_out_count
            + self.rtx.tx_out_ser
            + self.rtx.lock_time
            + struct.pack("<L", 1)

            )

        #hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.raw_tx_string).digest()).digest()
        #print(binascii.hexlify(hashed_tx_to_sign).decode('utf-8'))
        

        real_trx_inputs = bytes.fromhex('')
        i = 0
        for trx_in in  self.rtx.tx_ins:
            #print(self.rtx.tx_ins) #!!!!
            if i >= len(prv_txid):
                break
            #print("trx_in: ", trx_in)
            #print("self.rtx.tx_ins: ", self.rtx.tx_ins)
            hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.make_raw_trx_index(i)).digest()).digest() #!!!!
            sender_private_key = decode_58(privkey)[2:]
            #print(sender_private_key)
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(sender_private_key), curve = ecdsa.SECP256k1)
            vk = sk.verifying_key
            public_key = w.pubkey_from_privkey(int(sender_private_key, 16), 1)
            #print("public_key: ", public_key)
            signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)
            
            sigscript = (
            
                signature
                + bytes.fromhex("01")
                +  struct.pack("<B", len(public_key))
                + bytes.fromhex(public_key)
                )
            real_trx_inputs = ( real_trx_inputs
                + trx_in["txouthash"]
                + trx_in["tx_out_index"]
                + struct.pack("<B", len(sigscript) + 1)
                + struct.pack("<B", len(signature) + 1)
                + sigscript
                + trx_in["sequence"])
            i += 1

        self.real_tx = (

            self.rtx.version
            + self.rtx.tx_in_count
            + real_trx_inputs
            + self.rtx.tx_out_count
            + self.rtx.tx_out_ser
            + self.rtx.lock_time
            
            )

        #print(binascii.hexlify(self.real_tx).decode('utf-8'))
        hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.real_tx).digest()).digest()
        #print(binascii.hexlify(hashed_tx_to_sign).decode('utf-8'))
    
    def make_raw_trx_index(self, index):
        rtx1 = raw_tx_index()
        #print("rtx1: ", rtx1.tx_ins)
        i = 0
        for prv_tx in self.prv_txid:
            #print(self.rtx.tx_ins)
            rtx1.tx_ins.append({})
            #print(self.sender_hashed_pubkey)
            rtx1.tx_ins[i]["txouthash"] = bytes.fromhex(self.flip_byte_order(prv_tx))
            rtx1.tx_ins[i]["tx_out_index"] = struct.pack("<L",  self.tx_out_index[i]) # which nb of input we want to spend
            rtx1.tx_ins[i]["script"] = bytes.fromhex("76a914%s88ac" % self.sender_hashed_pubkey)#OP_DUP (76) OP_HASH160 (a9) len of next var (20 == 0x14) OP_EQUALVERIFY (88) OP_CHECKSIG (ac)
            rtx1.tx_ins[i]["script_bytes"] = struct.pack("<B", len(rtx1.tx_ins[i]["script"]))
            #print(binascii.hexlify(rtx1.tx_ins[i]["script"]).decode('utf-8'))
            rtx1.tx_ins[i]["sequence"] = bytes.fromhex("ffffffff")
            rtx1.tx_in_ser = ( rtx1.tx_in_ser
                + rtx1.tx_ins[i]["txouthash"]
                + rtx1.tx_ins[i]["tx_out_index"] 
                + rtx1.tx_ins[i]["script_bytes"]
                + rtx1.tx_ins[i]["script"]
                + rtx1.tx_ins[i]["sequence"] ) if i == index else \
                ( rtx1.tx_in_ser
                + rtx1.tx_ins[i]["txouthash"]
                + rtx1.tx_ins[i]["tx_out_index"]
                + rtx1.tx_ins[i]["sequence"] )
            i += 1
        rtx1.tx_in_count = struct.pack("<B", i)
        
        i = 0
        for recipient in self.recipients:
            #print("recipient: ", recipient)
            rtx1.tx_outs.append({})
            recipient_hashed_pubkey = binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')
            rtx1.tx_outs[i]["value"] = struct.pack("<Q", self.amounts[i]) #amount to send in output1
            rtx1.tx_outs[i]["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
            rtx1.tx_outs[i]["pk_script_bytes"] =  struct.pack("<B", len(rtx1.tx_outs[i]["pk_script"]))
            rtx1.tx_out_ser = ( rtx1.tx_out_ser
                + rtx1.tx_outs[i]["value"]
                + rtx1.tx_outs[i]["pk_script_bytes"]
                + rtx1.tx_outs[i]["pk_script"])
            i += 1
        rtx1.tx_out_count = struct.pack("<B", i)

        raw_tx_string = (

            rtx1.version
            + rtx1.tx_in_count
            + rtx1.tx_in_ser
            + rtx1.tx_out_count
            + rtx1.tx_out_ser
            + rtx1.lock_time
            + struct.pack("<L", 1)

            )
        return raw_tx_string

    def flip_byte_order(self, string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped

    def greedy(self, amount, prv_txid, tx_out_index, value):
        total = 0
        prv_txid_rez = []
        tx_out_index_rez = []
        for i in range(len(prv_txid)):
            prv_txid_rez.append(prv_txid[i])
            tx_out_index_rez.append(tx_out_index[i])
            total += value[i]
            #print(total)
            if total >= amount + fee:
                return prv_txid_rez, tx_out_index_rez, total
        return [], [], 0


    def get_prv_txid(self, sender, recipients, amounts, prv_txid, tx_out_index):
        if prv_txid == '0':
            try:
                f = open('url', 'r')
                URL = f.readline().rstrip('\n')
            except:
                URL = 'http://127.0.0.1:5000'
            url  = URL + '/utxo'
            payload = {"adress": sender, "amount": amounts[0]}
            headers = {"Content-Type": "application/json"}
            res = requests.get(url, json=payload, headers=headers)
            # получаем массивы:
            # prv_txid[] - все непотраченные выходы сендера (0 и более)
            # tx_out_index[] - индексы, соответствующие этим выходам (0 и более)
            # value[] - суммы, соответствующие этим выходам (0 и более)
            prv_txid = json.loads(res.text)['prv_txid']
            tx_out_index = json.loads(res.text)['tx_out_index']
            value = json.loads(res.text)['balance']
            #print(prv_txid, '\n', tx_out_index, '\n', value)

            prv_txid_rez, tx_out_index_rez, total = self.greedy(amounts[0], prv_txid, tx_out_index, value)
            #print("total: ", total)
            if amounts[0] + fee < total:
                recipients.append(sender)
                amounts.append(total - amounts[0]- fee)
            return prv_txid_rez, tx_out_index_rez
        else:
            return [prv_txid,], [tx_out_index,]

    def normalize_secret_bytes(privkey_bytes: bytes) -> bytes:
        scalar = string_to_number(privkey_bytes) % CURVE_ORDER
        if scalar == 0:
            raise Exception('invalid EC private key scalar: zero')
        privkey_32bytes = number_to_string(scalar, CURVE_ORDER)
        return privkey_32bytes
    '''
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
    '''
class CoinbaseTransaction(Transaction):

    def __init__(self, recipient, amount=50*10**8):
        hashed_pubkey =  binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')[2:]
        #print("---->>>", hashed_pubkey)
        self.rtx = raw_tx()
        self.rtx.tx_ins.append({})
        self.rtx.tx_ins[0]["txouthash"] = bytes.fromhex('0'*64)
        self.rtx.tx_ins[0]["sequence"] = bytes.fromhex("ffffffff")
        self.rtx.tx_ins[0]["coinbase"] = os.urandom(15)
        self.rtx.tx_ins[0]["coinbase_bytes"] = struct.pack("<B", len(self.rtx.tx_ins[0]["coinbase"]))

        self.rtx.tx_outs.append({})
        self.rtx.tx_outs[0]["value"] = struct.pack("<Q", amount) #amount to send in output1
        self.rtx.tx_outs[0]["pk_script"] = bytes.fromhex("76a914%s88ac" % hashed_pubkey)
        self.rtx.tx_outs[0]["pk_script_bytes"] =  struct.pack("<B", len(self.rtx.tx_outs[0]["pk_script"]))

        self.raw_tx_string = (

            self.rtx.version
            + self.rtx.tx_in_count
            + self.rtx.tx_ins[0]["txouthash"]
            + self.rtx.tx_ins[0]["sequence"]
            + self.rtx.tx_ins[0]["coinbase_bytes"]
            + self.rtx.tx_ins[0]["coinbase"]
            + self.rtx.tx_ins[0]["sequence"]
            + self.rtx.tx_out_count
            + self.rtx.tx_outs[0]["value"]
            + self.rtx.tx_outs[0]["pk_script_bytes"]
            + self.rtx.tx_outs[0]["pk_script"]
            + self.rtx.lock_time

            )
        self.raw_tx_string = binascii.hexlify(self.raw_tx_string).decode('utf-8')
        #print(self.raw_tx_string)

if __name__ == "__main__":
    key = "cV9zX345UyzDgf3BEGBNxUhevXFMnDdfY5QwMp8KzXabAXnCz6ir"
    privkey_hex = binascii.hexlify(base58.b58decode_check(key)[2:]).decode('utf-8')
    #print(len(privkey_hex))
    trx = Transaction("2MtmAWWJzTPQwiPqjiBNeX3JfeCPsGNAn1q", ["18jjnHjdQgG5K5YYJ36t8Fiu4MUWo5wWQN",], [900000,], privkey_hex)