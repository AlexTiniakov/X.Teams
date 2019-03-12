import initializer
import miner_cli as mc
import wallet_cli as wc
import wallet as w
import os
import requests
from flask import json
from serializer import Deserializer
import binascii
from pending_pool import show_mem

URL = 'http://127.0.0.1:5000'

def run():
    print("====================================================")
    print("|                   TEST 1                         |")
    print("|init new private key, make public key and address |")
    print("====================================================")
    wallet = wc.Wallet()
    wallet.do_new("")
    print("====================================================")
    print("|                   TEST 2                         |")
    print("|  save information to files address and minerkey  |")
    print("====================================================")
    wallet.do_save("")
    f = open('address', 'r')
    print("file 'address':  ", f.readline())
    f = open('minerkey', 'r')
    print("file 'minerkey': ", f.readline())
    print("====================================================")
    print("|                   TEST 3                         |")
    print("|           import minerkey to wallet              |")
    print("====================================================")
    wallet.do_import("minerkey")
    print("====================================================")
    print("|                   TEST 4                         |")
    print("|         check balance (must be 0!)               |")
    print("====================================================")
    wallet.do_balance("")
    print("====================================================")
    print("|                   TEST 5                         |")
    print("|           lets mine some coins!                  |")
    print("====================================================")
    miner = mc.Miner()
    print("\n     hash of mined block is:\n")
    miner.do_mine("")
    print("\n     and block loocks like this:\n")
    blocks = requests.get(URL + '/chain')
    blocks = json.loads(blocks.text)['blocks']
    print(blocks[-1])
    print("\n     and your transaction:\n")
    trx = Deserializer(blocks[-1]["transactions"][0]).trx
    print(trx, "\n\n     Congratulations!!! Your balance in satoshies is:\n")
    print(trx['outputs'][0]['value'])
    print("====================================================")
    print("|                   TEST 6                         |")
    print("|           check balance againe!                  |")
    print("====================================================")
    print("\nYour current ballance from UTXO (in satoshies) is:\n")
    wallet.do_balance("")
    print("====================================================")
    print("|                   TEST 7                         |")
    print("|Now it's time to send some pitcoins to your friend|")
    print("====================================================")
    print("Form transaction to adress, for example: \n1Bh7Pn4kBGkNza9oBEHa4t3LiDan8REUzQ")
    print("let's send 10000 satoshies. First form transaction. Serialized tx:")
    wallet.do_send("1Bh7Pn4kBGkNza9oBEHa4t3LiDan8REUzQ 10000")
    print("Deserialized tx:")
    print(Deserializer(binascii.hexlify(wallet.tr.real_tx).decode('utf-8')).trx)
    print("then, let's broadcast it...")
    wallet.do_broadcast(binascii.hexlify(wallet.tr.real_tx).decode('utf-8'))
    print("and check mempool...")
    print(show_mem())
    print("====================================================")
    print("|                   TEST 8                         |")
    print("|     Next, mine block with your transaction       |")
    print("====================================================")
    print("mined block hash is:")
    miner.do_mine("")
    print("mempool (empty, really??):")
    print(show_mem())
    print("Your ballance is:")
    wallet.do_balance("")
    print("And balance 1Bh7Pn4kBGkNza9oBEHa4t3LiDan8REUzQ is:")
    wallet.do_balance("1Bh7Pn4kBGkNza9oBEHa4t3LiDan8REUzQ")
    print("full UTXO you can see in browser: http://127.0.0.1:5000/utxo")

if __name__ == "__main__":
    run()