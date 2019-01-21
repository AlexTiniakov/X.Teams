def decode_base58(x):
    base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    rez = "5"
    while(x >= 1):
        rez += base58[int(x % 58)]
        x /= 58
    return rez

def read_privkey():
    f = open('privkey')
    pk = f.readline()
    x = int(pk, 16)
    print(x)
    rez = decode_base58(x)
    print(rez)

if __name__ == "__main__":
    read_privkey()