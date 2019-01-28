import sqlite3 as sql
from tx_validator import validate
from serializer import Deserializer

def get_from_mem():
    try:
        f = open('transaction/pending', 'r')
    except IOError:
        return ''
    mem = f.readlines()
    f.close()
    f = open('transaction/pending', 'w')
    rez = []
    for i in mem:
        rez.append(i.rstrip('\n'))
        if len(rez) == 3:
            break
    for i in range(len(rez)):
        del(mem[0])
    for i in mem:
        f.write(i)
    f.close()
    return rez

def show_mem():
    try:
        f = open('transaction/pending', 'r')
    except IOError:
        return ''
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip('\n')
    return lines

def add_to_mem(ser):
    f = open('transaction/pending', 'a')
    f.write(ser + '\n')
    f.close()
    return 'transaction sucsessfuly added to mempyl'

def assept(ser):
    trx = Deserializer(ser).trx
    if validate(trx):
        add_to_mem(ser)
        return True
    else:
        return False
        
    