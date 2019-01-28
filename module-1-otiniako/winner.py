import hashlib
import ecdsa
import binascii
from ecdsa import SigningKey, VerifyingKey, BadSignatureError

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

def sign_message(privkey, message):
    sk = SigningKey.from_string(binascii.unhexlify(privkey), curve=SECP256k1)
    vk = sk.get_verifying_key()
    pubkey_sig = binascii.hexlify(vk.to_string()).decode('utf-8')
    sig = binascii.hexlify(sk.sign(bytes(message, 'ascii'))).decode('utf-8')
    sig = binascii.hexlify(sk.sign(bytes(message, 'ascii'))).decode('utf-8')
    print(sig)
    print(pubkey_sig)


privkey = hashlib.sha256(bytes('otiniako', 'ascii')).hexdigest()
sign_message(privkey, 'grudger')
