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
        amount = int(amount, 16)
    except ValueError:
        return False
    if amount > 0 and amount < 21*10**6:
        return True
    return False

def hash(trx):
    if len(trx[1]) == 0:
        trx[1] =  '0'*35
    to_hash = trx[1] + trx[2] + trx[0]
    return hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

def validate(trx):
    if trx[1] == '0'*35:
        if verify_pubkey_addr(trx[2], trx[3]) and \
        check_amount(trx[0]) and \
        check_sig(trx[3], trx[4], hash(trx)):
            return True
        else:
            return False
    if len(trx[1]) > 0 and verify_addr(trx[1]) and \
        verify_addr(trx[2]) and \
        verify_pubkey_addr(trx[1], trx[3]) and \
        check_amount(trx[0]) and \
        check_sig(trx[3], trx[4], hash(trx)):
        return True
    else:
        return False