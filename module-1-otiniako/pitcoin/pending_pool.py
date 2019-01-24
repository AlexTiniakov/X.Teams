import sqlite3 as sql
from tx_validator import validate

def del_zero(buf):
    while buf[0]=='0':
        buf = buf[1:]
    return buf

def get_from_mem():
    try:
        f = open('mempool', 'r')
    except IOError:
        return ''
    mem = f.readlines()
    f.close()
    f = open('mempool', 'w')
    rez = []
    for i in mem:
        rez.append(i[:-2])
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
        f = open('mempool', 'r')
    except IOError:
        return ''
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = lines[i][:-2]
    return lines

def add_to_mem(ser):
    f = open('mempool', 'a')
    f.write(ser + '\n')
    f.close()

def assept(ser):
    trx = []
    trx.append(del_zero(ser[0:4]))
    trx.append(del_zero(ser[4:39]))
    trx.append(del_zero(ser[39:74]))
    trx.append(del_zero(ser[74:202]))
    trx.append(del_zero(ser[202:]))
    #print('assert: ', trx[4])
    if validate(trx):
        add_to_mem(ser)
    