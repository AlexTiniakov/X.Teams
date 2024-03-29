import hashlib
import random
import binascii
import ecdsa
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from ecdsa.util import string_to_number, number_to_string
import os
import codecs
import base58 as b58
base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1,
oid_secp256k1)
ec_order = _r
curve = curve_secp256k1
generator = generator_secp256k1

# from b58check to hex
def decode_58(string):
    bits = b58.b58decode_check(string)
    rez = binascii.hexlify(bits).decode('utf-8')
    return rez

# from hex to b58check
def encode_58(string):
    bits = b58.b58encode_check(bytes.fromhex(string))
    return bits.decode('utf-8')

# Decoding key from hex format to base58heck
def decode_base58(pk, public=0):
    pk = "80" + pk if public==0 else pk
    #print(pk)
    h1 = hashlib.sha256(binascii.unhexlify(pk)).hexdigest()
    h2 = hashlib.sha256(binascii.unhexlify(h1)).hexdigest()
    pk += h2[0:8]
    leading_zeros = len(pk) - len(pk.lstrip('0'))
    ones = leading_zeros // 2
    x = int(pk, 16)
    rez = ''
    while x:
        x, idx = divmod(x, 58)
        rez = base58[idx:idx+1] + rez
    if public==1:
        for one in range(ones):
            rez = '1' + rez
    return str(rez)

def decode_hex(pk):
    rez = 0
    for c in pk:
        rez *= 58
        rez += base58.index(c)
    rez = hex(rez)[4:len(str(rez))-21]
    if len(rez) % 2 == 1:
        rez = "0" + rez
    return rez

# Read private key from file in hex, return in base58check format
def read_privkey(compress=0):
    try:
        f = open('privkey')
    except IOError:
        print("Error: can\'t find file or read data")
    pk = f.readline()
    if compress==1:
        pk = pk + "01" 
    rez = decode_base58(pk)
    return rez

# Generate a new private key and return it in int format
def random_privkey():
    byte_array = os.urandom(32)
    return int(binascii.hexlify(byte_array), 16)

# Get the compressed public key from the point.
def get_point_pubkey(point):
    # if y < 0 -> key == 03*; else key == 02*
    if point.y() & 1:
        key = '03' + '%064x' % point.x()
    else:
        key = '02' + '%064x' % point.x()
    return key

# Get the uncompressed public key from the point.
def get_point_pubkey_uncompressed(point):
    # Uncompressed public key looks like 04*
    key = '04' + \
        '%064x' % point.x() + \
        '%064x' % point.y()
    return key

# Get the public key from private key
def pubkey_from_privkey(privkey, compress=0):
    # Get the public key point on the curve.
    point = privkey * generator
    # Get the public key from the point.
    pubkey = get_point_pubkey(point) if compress==1 else get_point_pubkey_uncompressed(point)
    return pubkey

# Get the public address from public key (in hex format).
def addr_from_pubkey(pubkey):
    h1 = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()
    h2 = hashlib.new('ripemd160')
    h2.update(binascii.unhexlify(h1))
    h2 = h2.hexdigest()
    return decode_base58('00' + h2, 1)

# Get the public address from private key (in int format).
def addr_from_privkey(privkey, compress=0):
    pubkey = pubkey_from_privkey(privkey, compress)
    return addr_from_pubkey(pubkey)

def sign_message(privkey, message):
    sk = SigningKey.from_string(binascii.unhexlify(privkey), curve=SECP256k1)
    vk = sk.get_verifying_key()
    pubkey_sig = binascii.hexlify(vk.to_string()).decode('utf-8')
    sig = binascii.hexlify(sk.sign(message)).decode('utf-8')
    #sig = binascii.hexlify(sk.sign(bytes(message, 'ascii'))).decode('utf-8')
    return sig, pubkey_sig

def check_sig(pubkey_sig, sig, message):
    sig = binascii.a2b_hex(sig)
    vk = VerifyingKey.from_string(bytes.fromhex(pubkey_sig), curve=ecdsa.SECP256k1)
    try:
        vk.verify(sig, bytes(message, 'ascii'))
        return True
    except BadSignatureError:
        print('Error: Bad signature!')
        return False

    
