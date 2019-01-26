import hashlib

def merkle_root(buf):
    #print(buf, '\n')
    if len(buf)==1 and len(buf[0]) <= 64:
        return buf
    elif len(buf) % 2 == 1:
        buf.append(buf[-1])
        return merkle_root(buf)
    else:
        buf_new = []
        for i in range(int(len(buf)/2)):
            to_hash = buf[i] + buf[i+1]
            buf_new.append(hashlib.sha256(to_hash.encode('utf-8')).hexdigest())
        return merkle_root(buf_new)