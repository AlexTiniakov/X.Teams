import hashlib
import random
import binascii
import ecdsa
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from ecdsa.util import string_to_number, number_to_string
import os
import codecs

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

# Decoding key from hex format to base58heck
def decode_base58(pk, public=0):
    base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
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

# Read private key from file in hex, return in base58check format
def read_privkey(compress=0):
    f = open('privkey')
    pk = f.readline()
    pk = "80" + pk
    if compress==1:
        pk = pk + "01" 
    print(pk)
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
        key = '04' + \
              '%064x' % point.x() + \
              '%064x' % point.y()
        return key

# Get the public key.
def pubkey_from_privkey(privkey, compress=0):
    # Get the public key point on the curve.
    point = privkey * generator
    # Get the public key from the point.
    pubkey = get_point_pubkey(point) if compress==1 else get_point_pubkey_uncompressed(point)
    return pubkey

# Get the public address from private key.
def addr_from_privkey(privkey, compress=0):
    pubkey = pubkey_from_privkey(privkey, compress)
    h1 = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()
    h2 = hashlib.new('ripemd160')
    h2.update(binascii.unhexlify(h1))
    h2 = h2.hexdigest()
    #print(h2)
    return decode_base58('00' + h2, 1)

def sign_message(privkey, message):
    sk = SigningKey.from_string(binascii.unhexlify(privkey), curve=SECP256k1)
    vk = sk.get_verifying_key()
    pubkey = binascii.hexlify(vk.to_string()).decode('utf-8')
    sig = sk.sign(bytes(message, 'ascii'))
    return sig, pubkey

def check_sig(pubkey, sig, message):
    vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=ecdsa.SECP256k1)
    try:
        vk.verify(sig, bytes(message, 'ascii'))
        print ("good signature")
    except BadSignatureError:
        print ("BAD SIGNATURE")


if __name__ == "__main__":
    read_key = read_privkey()
    #print(read_key)
    #privkey = 38090835015954358862481132628887443905906204995912378278060168703580660294000
    privkey = '3aba4162c7251c891207b747840551a71939b0de081f85c4e44cf7c13e41daa6'
    sig, pubkey = sign_message(privkey, "hello")
    check_sig(pubkey, sig, "hello")
    #privkey = random_privkey()
    #pubkey = pubkey_from_privkey(privkey, 1)
    #print(pubkey)
    #print(addr_from_privkey(privkey))

    