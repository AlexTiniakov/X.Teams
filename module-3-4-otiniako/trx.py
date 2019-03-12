class raw_tx:
    version = struct.pack("<L", 1)
    tx_in_count = struct.pack("<B", 1)
    tx_in= {} #TEMP
    tx_out_count = struct.pack("<B", 2)
    tx_out1= {} #TEMP
    tx_out2     = {} #TEMP
    lock_time   = struct.pack("<L", 0)


# Alise -> Bob -> Charlie
# Alise - previous trx

    Bob_addr = "1AKWncNgFgTNBe3ufqH16GSDf9WeGkJSLY" # sender

bob_hashed_pubkey = binascii.hexlify(base58.b58decode_check(Bob_addr)[1:]).decode('utf-8')
#print(bob_hashed_pubkey)
#print("76a914%s88ac" % bob_hashed_pubkey)
Bob_private_key = "bf08e6e2ae86ef360f1f40c3b721203e5f56f8dcb7641f78e82b4bf097800aaa"

prv_txid = "78f0066a34162b604f99b21d8c0f5b27841854ea5220a41cd36b3ab07d6df1ba" #referense to prev trx (prev trx hash)

Charlie_addr = "17JaFGEmdt5B72wbASPvk28Y154rByd3Xg" # resipient

charlie_hashed_pubkey =  binascii.hexlify(base58.b58decode_check(Charlie_addr)[1:]).decode('utf-8')

# 1. raw_tx
# 2. raw_tx and sign that tx using my private key
# 3. raw tx and signature in order to create the real tx

def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
    return flipped

rtx = raw_tx()

rtx.tx_in["txouthash"] = bytes.fromhex(flip_byte_order(prv_txid))
rtx.tx_in["tx_out_index"] = struct.pack("<L", 0) # which nb of input we want to spend
rtx.tx_in["script"] = bytes.fromhex("76a914%s88ac" % bob_hashed_pubkey) #OP_DUP (76) OP_HASH160 (a9) len of next var (20 == 0x14) OP_EQUALVERIFY (88) OP_CHECKSIG (ac)
rtx.tx_in["script_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
rtx.tx_in["sequence"] = bytes.fromhex("ffffffff")

rtx.tx_out1["value"] = struct.pack("<Q", 100000) #amount to send in output1
rtx.tx_out1["pk_script"] = bytes.fromhex("76a914%s88ac" % charlie_hashed_pubkey)
rtx.tx_out1["pk_script_bytes"] =  struct.pack("<B", len(rtx.tx_out1["pk_script"]))

rtx.tx_out2["value"] = struct.pack("<Q", 50000) #amount to send in output1
rtx.tx_out2["pk_script"] = bytes.fromhex("76a914%s88ac" % bob_hashed_pubkey)
rtx.tx_out2["pk_script_bytes"] =  struct.pack("<B", len(rtx.tx_out2["pk_script"]))
'''
print(type(rtx.version),
    type(rtx.tx_in_count),
    type(rtx.tx_in["txouthash"]),
    type(rtx.tx_in["tx_out_index"]),
    type(rtx.tx_in["script_bytes"]),
    type(rtx.tx_in["script"]),
    type(rtx.tx_in["sequence"]),
    type(rtx.tx_out_count),
    type(rtx.tx_out1["value"]),
    type(rtx.tx_out1["pk_script_bytes"]),
    type(rtx.tx_out1["pk_script"]),
    type(rtx.tx_out2["value"]),
    type(rtx.tx_out2["pk_script_bytes"]),
    type(rtx.tx_out2["pk_script"]),
    type(rtx.lock_time),
    type(struct.pack("<L", 1)))
'''
raw_tx_string = (

    rtx.version
    + rtx.tx_in_count
    + rtx.tx_in["txouthash"]
    + rtx.tx_in["tx_out_index"]
    + rtx.tx_in["script_bytes"]
    + rtx.tx_in["script"]
    + rtx.tx_in["sequence"]
    + rtx.tx_out_count
    + rtx.tx_out1["value"]
    + rtx.tx_out1["pk_script_bytes"]
    + rtx.tx_out1["pk_script"]
    + rtx.tx_out2["value"]
    + rtx.tx_out2["pk_script_bytes"]
    + rtx.tx_out2["pk_script"]
    + rtx.lock_time
    + struct.pack("<L", 1)

    )

hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(raw_tx_string).digest()).digest()

sk = ecdsa.SigningKey.from_string(bytes.fromhex(Bob_private_key), curve = ecdsa.SECP256k1)
vk = sk.verifying_key
public_key = ('04' + binascii.hexlify(vk.to_string()).decode('utf-8'))
signature = sk.sign_digest(hashed_tx_to_sign, sigencode = ecdsa.util.sigencode_der)

sigscript = (
    signature
    + bytes.fromhex("01")
    +  struct.pack("<B", len(public_key))
    + bytes.fromhex(public_key)
    )

real_tx = (

    rtx.version
    + rtx.tx_in_count
    + rtx.tx_in["txouthash"]
    + rtx.tx_in["tx_out_index"]
    + struct.pack("<B", len(sigscript) + 1)
    + struct.pack("<B", len(signature) + 1)
    + sigscript
    + rtx.tx_in["sequence"]
    + rtx.tx_out_count
    + rtx.tx_out1["value"]
    + rtx.tx_out1["pk_script_bytes"]
    + rtx.tx_out1["pk_script"]
    + rtx.tx_out2["value"]
    + rtx.tx_out2["pk_script_bytes"]
    + rtx.tx_out2["pk_script"]
    + rtx.lock_time
    
    )

#print(prv_txid)
#print(rtx.tx_in["txouthash"])

#print(binascii.hexlify(real_tx).decode('utf-8'))
