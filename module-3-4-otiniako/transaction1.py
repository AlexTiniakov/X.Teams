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
from enum import Enum
from ecdsa.util import string_to_number, number_to_string
from ecdsa.curves import SECP256k1

CURVE_ORDER = SECP256k1.order
fee = 1000

URL = 'http://127.0.0.1:5000'

class raw_tx:
            version 	    = struct.pack("<L", 1)
            tx_in_count     = struct.pack("<B", 1)
            tx_ins	        = [] #TEMP
            tx_in_ser       =  bytes.fromhex("")
            tx_out_count    = struct.pack("<B", 1)
            tx_outs	        = [] #TEMP
            tx_out_ser      =  bytes.fromhex("")
            lock_time       = struct.pack("<L", 0)
            raw_tx_string   = ""

class Transaction(object):

    def __init__(self, sender, recipients, amounts, privkey, prv_txid='0', tx_out_index=0):
        self.rtx = raw_tx()
        self.rtxs = []
        self.rtx_sign = []
        self.raw_tx_string = []
        self.sender_address = sender # "mv3d5P4kniPrT5owreux438yEtcFUefo71"
        self.recipients = recipients # ["n3Jqa2cyGqKDvc8QNMKYooy5yYUqoGwrvi", "mv3d5P4kniPrT5owreux438yEtcFUefo71"]
        self.amounts = amounts # [100, 9000]
        self.sender_wif_priv = privkey # "5JrJuxQ5QhLASMpQgSCZ9Fmzt8Sit8X3h1N9LGWYdXDtBhUxCwB"
        sender_private_key = decode_58(privkey)[2:]
        print("sender_private_key: ", sender_private_key)
        #self.sender_priv = 
        print("transaction 1")
        # получам такие массивы:
        # recipients[] - 1 или 2 в зависимости от того, есть ли здача
        # amounts[] - 1 или 2 в зависимости от того, есть ли здача
        # prv_txid[] - 0, 1 или более в зависимости от найденных непотраченных выходов
        # tx_out_index[] индексы, соответствующие выходам
        prv_txid, tx_out_index = self.get_prv_txid(sender, recipients, amounts, prv_txid, tx_out_index)

        print("Inputs:")
        print("prv_txid: ", prv_txid)
        print("tx_out_index: ", tx_out_index)

        sender_hashed_pubkey = decode_58(sender)
        
        '''# сформируем raw_trx без скриптов вообще (self.rtx)
        self.form_raw_trx(sender, recipients, amounts, prv_txid, tx_out_index)

        # для каждого инпута подготовим транзакцию для подписания.
        # Для этого включим скрипт проверки поочередно для каждого инпута
        for i in range(len(prv_txid)):
            self.rtx_sign.append(self.rtx)
            self.form_raw_trx_to_sign(i)
        self.rtx = self.form_raw_trx()'''

        #для каждого инпута формируем свою raw_trx для подписи
        for j in range(len(prv_txid)):
            i = 0
            rtx = raw_tx()
            for prv_tx in prv_txid:
                rtx.tx_ins.append({})
                print("prv_txid: ", prv_tx)
                rtx.tx_ins[i]["txouthash"] = bytes.fromhex(self.flip_byte_order(prv_tx))
                rtx.tx_ins[i]["tx_out_index"] = struct.pack("<L",  tx_out_index[j]) # which nb of input we want to spend
                rtx.tx_ins[i]["script"] = bytes.fromhex("76a914%s88ac" % sender_hashed_pubkey) if i == j else bytes.fromhex("") #OP_DUP (76) OP_HASH160 (a9) len of next var (20 == 0x14) OP_EQUALVERIFY (88) OP_CHECKSIG (ac)
                rtx.tx_ins[i]["script_bytes"] = struct.pack("<B", len(rtx.tx_ins[i]["script"])) if i == j else bytes.fromhex("")
                #print(len(rtx.tx_ins[i]["script"]))
                rtx.tx_ins[i]["sequence"] = bytes.fromhex("ffffffff")
                rtx.tx_in_ser = ( rtx.tx_in_ser
                    + rtx.tx_ins[i]["txouthash"]
                    + rtx.tx_ins[i]["tx_out_index"]
                    + rtx.tx_ins[i]["script_bytes"]
                    + rtx.tx_ins[i]["script"]
                    + rtx.tx_ins[i]["sequence"] )
                i += 1
            rtx.tx_in_count = struct.pack("<B", len(prv_txid))
            i = 0
            for recipient in recipients:
                #print("recipient: ", recipient)
                rtx.tx_outs.append({})
                recipient_hashed_pubkey = binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')
                rtx.tx_outs[i]["value"] = struct.pack("<Q", amounts[i]) #amount to send in output1
                rtx.tx_outs[i]["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
                rtx.tx_outs[i]["pk_script_bytes"] =  struct.pack("<B", len(rtx.tx_outs[i]["pk_script"]))
                rtx.tx_out_ser = ( rtx.tx_out_ser
                    + rtx.tx_outs[i]["value"]
                    + rtx.tx_outs[i]["pk_script_bytes"]
                    + rtx.tx_outs[i]["pk_script"])
                i += 1
            rtx.tx_out_count = struct.pack("<B", i)

            rtx.raw_tx_string = (

                rtx.version
                + rtx.tx_in_count
                + rtx.tx_in_ser
                + rtx.tx_out_count
                + rtx.tx_out_ser
                + rtx.lock_time
                + struct.pack("<L", 1)

                )
            print("raw_tx_string: ", binascii.hexlify(rtx.raw_tx_string).decode('utf-8'))
            self.rtxs.append(rtx)

        #hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.raw_tx_string).digest()).digest()
        #print(binascii.hexlify(hashed_tx_to_sign).decode('utf-8'))
        

        real_trx_inputs = bytes.fromhex('')
        i = 0
        print("len(self.rtx.tx_ins): ", len(self.rtxs))
        for j in range(len(self.rtxs)):
            hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.rtxs[i].raw_tx_string).digest()).digest()
            print(hashed_tx_to_sign, "\n", sender_private_key)
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(sender_private_key), curve = ecdsa.SECP256k1)
            vk = sk.verifying_key
            public_key = ('04' + binascii.hexlify(vk.to_string()).decode('utf-8'))
            signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)
            
            sigscript = (
            
                signature
                + bytes.fromhex("01")
                +  struct.pack("<B", len(bytes.fromhex(public_key)))
                + bytes.fromhex(public_key)
                )
            print( type(real_trx_inputs),
                type(prv_txid[j]),
                type(tx_out_index[j]),
                type(struct.pack("<B", len(sigscript) + 1)),
                type(struct.pack("<B", len(signature) + 1)),
                type(sigscript),
                type(self.rtxs[j].tx_ins[i]["sequence"]))

            print( (real_trx_inputs),
                (prv_txid[j]),
                (tx_out_index[j]),
                (struct.pack("<B", len(sigscript) + 1)),
                (struct.pack("<B", len(signature) + 1)),
                (sigscript),
                (self.rtxs[j].tx_ins[i]["sequence"]))
            
            print("self.rtxs[j].tx_ins[i][\"sequence\"]: ", self.rtxs[j].tx_ins[i]["sequence"])
            print("bytes.fromhex(prv_txid[j]): ", bytes.fromhex(prv_txid[j]))
            print("bytes.fromhex(hex(tx_out_index[j])[2:]): ", hex(tx_out_index[j])[2:].rjust(2, '0'))
            real_trx_inputs = ( real_trx_inputs
                + bytes.fromhex(prv_txid[j])
                + bytes.fromhex(hex(tx_out_index[j])[2:].rjust(2, '0'))
                + struct.pack("<B", len(sigscript) + 1)
                + struct.pack("<B", len(signature) + 1)
                + sigscript
                + self.rtxs[j].tx_ins[i]["sequence"])
            print("real_trx_inputs: ", real_trx_inputs)
            i += 1

        self.real_tx = (

            self.rtx.version
            + self.rtxs[0].tx_in_count
            + real_trx_inputs
            + self.rtx.tx_out_count
            + self.rtx.tx_out_ser
            + self.rtx.lock_time
            
            )
        '''#print(binascii.hexlify(hashed_tx_to_sign).decode('utf-8'))
        

        real_trx_inputs = bytes.fromhex('')
        i = 0
        for trx_in in  self.rtx.tx_ins:
            hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(self.raw_tx_string).digest()).digest()
            sender_private_key = privkey
            #print(sender_private_key)
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(sender_private_key), curve = ecdsa.SECP256k1)
            vk = sk.verifying_key
            public_key = ('04' + binascii.hexlify(vk.to_string()).decode('utf-8'))
            signature = sk.sign_digest(hashed_tx_to_sign, sigencode = ecdsa.util.sigencode_der)
            
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
        #print(binascii.hexlify(hashed_tx_to_sign).decode('utf-8'))'''
    
    def flip_byte_order(self, string):
        flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
        return flipped

    def normalize_secret_bytes(privkey_bytes: bytes) -> bytes:
        scalar = string_to_number(privkey_bytes) % CURVE_ORDER
        if scalar == 0:
            raise Exception('invalid EC private key scalar: zero')
        privkey_32bytes = number_to_string(scalar, CURVE_ORDER)
        return privkey_32bytes

    def form_raw_trx_to_sign(self, index):
        tx_in = self.rtx_sign[-1].tx_ins[index]
        tx_in["script"] = bytes.fromhex("76a914%s88ac" % self.sender_hashed_pubkey) #OP_DUP (76) OP_HASH160 (a9) len of next var (20 == 0x14) OP_EQUALVERIFY (88) OP_CHECKSIG (ac)
        tx_in["script_bytes"] = struct.pack("<B", len(tx_in["script"]))
        self.rtx.tx_in_ser = ( self.rtx.tx_in_ser
                + self.rtx.tx_ins[i]["txouthash"]
                + self.rtx.tx_ins[i]["tx_out_index"]
                + self.rtx.tx_ins[i]["script_bytes"]
                + self.rtx.tx_ins[i]["script"]
                + self.rtx.tx_ins[i]["sequence"] )
                


    def form_raw_trx(self, sender, recipients, amounts, prv_txid, tx_out_index, index):
        j = 0
        for i in range(len(prv_txid)):
            self.rtx.tx_ins.append({})
            self.rtx.tx_ins[i]["txouthash"] = bytes.fromhex(self.flip_byte_order(prv_txid[i]))
            self.rtx.tx_ins[i]["tx_out_index"] = struct.pack("<L",  tx_out_index[i])
            self.rtx.tx_ins[i]["sequence"] = bytes.fromhex("ffffffff")
            j += 1
            print("trabsaction.form_raw_trx.self.rtx.tx_ins: ",  self.rtx.tx_ins)
        self.rtx.tx_in_count = struct.pack("<B", len(prv_txid))
        
        i = 0
        for recipient in self.recipients:
            self.rtx.tx_outs.append({})
            recipient_hashed_pubkey = binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')
            self.rtx.tx_outs[i]["value"] = struct.pack("<Q", self.amounts[i]) #amount to send in output1
            self.rtx.tx_outs[i]["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
            self.rtx.tx_outs[i]["pk_script_bytes"] =  struct.pack("<B", len(self.rtx.tx_outs[i]["pk_script"]))
            self.rtx.tx_out_ser = ( self.rtx.tx_out_ser
                + self.rtx.tx_outs[i]["value"]
                + self.rtx.tx_outs[i]["pk_script_bytes"]
                + self.rtx.tx_outs[i]["pk_script"])
            i += 1
        self.rtx.tx_out_count = struct.pack("<B", i)
        print("transaction.form_raw_trx.self.rtx: ", self.rtx)
        
        self.raw_tx_string = (

            self.rtx.version
            + self.rtx.tx_in_count
            + self.rtx.tx_in_ser
            + self.rtx.tx_out_count
            + self.rtx.tx_out_ser
            + self.rtx.lock_time
            + struct.pack("<L", 1)

            )
        
        

    # найдем выход(ы) по алгоритму жадины (ну или хотя бы просто найдем)
    def greedy(self, amount, prv_txid, tx_out_index, value):
        total = 0
        prv_txid_rez = []
        tx_out_index_rez = []
        for i in range(len(prv_txid)):
            prv_txid_rez.append(prv_txid[i])
            tx_out_index_rez.append(tx_out_index[i])
            total += value[i]
            print(total)
            if total >= amount + fee:
                return prv_txid_rez, tx_out_index_rez, total
        return [], [], 0


    def get_prv_txid(self, sender, recipients, amounts, prv_txid, tx_out_index):
        if prv_txid == '0':
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
            print(prv_txid, '\n', tx_out_index, '\n', value)

            prv_txid_rez, tx_out_index_rez, total = self.greedy(amounts[0], prv_txid, tx_out_index, value)
            if amounts[0] + fee < total:
                recipients.append(sender)
                amounts.append(total - amounts[0]- fee)
            return prv_txid_rez, tx_out_index_rez
        else:
            return [prv_txid,], [tx_out_index,]

class CoinbaseTransaction(Transaction):

    def __init__(self, recipient, amount=50*10**8):
        hashed_pubkey =  binascii.hexlify(base58.b58decode_check(recipient)).decode('utf-8')
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
    #trx = Transaction("2MtmAWWJzTPQwiPqjiBNeX3JfeCPsGNAn1q", ["18jjnHjdQgG5K5YYJ36t8Fiu4MUWo5wWQN",], [900000,], privkey_hex)
    byte_array = os.urandom(32)
    string = binascii.hexlify(byte_array)
    print(string)
    print(encode_58("80"+privkey_hex))
