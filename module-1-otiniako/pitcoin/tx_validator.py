from wallet import addr_from_pubkey, check_sig
import hashlib

def verify_addr(addr):
    base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    if len(addr) > 35 or len(addr) < 26:
        return False
    for c in addr:
        if c not in base58:
            return False
    if addr[0] != '1' and addr[0] != '3':
        return False
    return True

def verify_pubkey_addr(addr, pubkey):
    if addr_from_pubkey('04' + pubkey) != addr:
        return False
    return True

def check_amount(amount):
    try:
        amount = float(amount)
    except ValueError:
        return False
    if amount > 0 and amount < 21*10**6:
        return True
    return False

def hash(trx):
    to_hash = trx[1] + trx[2] + trx[0]
    return hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

def validate(trx):
    if verify_addr(trx[1]) and \
        verify_addr(trx[2]) and \
        verify_pubkey_addr(trx[1], trx[3]) and \
        check_sig(trx[3], trx[4], hash(trx)) and \
        check_amount(trx[0]):
        #print('Ok')
        return True
    else:
        return False