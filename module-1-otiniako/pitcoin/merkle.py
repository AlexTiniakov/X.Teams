import hashlib

def merkle_root(buf):
    if len(buf)==1:
        return buf
    elif len(buf) % 2 == 1:
        buf.append(buf[-1])
        return merkle_root(buf)
    else:
        buf_new = []
        for i in range(len(buf)/2):
            to_hash = buf[i] + buf[i+1]
            buf_new.append(hashlib.sha256(to_hash.encode('utf-8')).hexdigest())
        return merkle_root(buf_new)