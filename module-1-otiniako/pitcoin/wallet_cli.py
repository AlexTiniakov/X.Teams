import sys
import cmd
import wallet as w
from transaction import Transaction
from tx_validator import validate
from serializer import Serializer
import pending_pool
import binascii
from pending_pool import show_mem, get_from_mem
import xmlrpc.client


server = xmlrpc.client.Server('http://localhost:8000')
class Wallet(cmd.Cmd):
    privkey_WIF = '0'
    
    def do_save(self, line):
        f = open('minerkey', 'w')
        if self.privkey_WIF != '0':
            f.write(str(self.privkey_WIF))
            print('Key was saved to file \'minerkey\'!\nStrongly recomend to protect this file!')
        else:
            print('Firstly create a new privkey with \'new\' or import it with \'import\'')
    
    def do_new(self, line):
        self.privkey_d = w.random_privkey()
        self.pubkey = w.pubkey_from_privkey(self.privkey_d, 0)
        self.addr = w.addr_from_privkey(self.privkey_d, 0)
        self.privkey_hex = hex(self.privkey_d)[2:]
        if len(self.privkey_hex) % 2 == 1:
            self.privkey_hex = "0" + self.privkey_hex
        self.privkey_WIF = w.decode_base58(self.privkey_hex)
        print('Private key (hex) is:\n ', self.privkey_hex)
        print('Private key (decimal) is:\n ', self.privkey_d)
        print('Private key (WIF) is:\n ', self.privkey_WIF)
        print('Public key (hex) is:\n ', self.pubkey)
        print('Pitcoin Address (b58check) is:\n ', self.addr)
        f = open('address', 'w')
        f.write(self.addr)
        f.close()
        print('If you want to save Private key to file enter \'save\'')

    def do_import(self, line):
        if (len(line)!=0):
            try:
                f = open(line, 'r')
                self.privkey_WIF = f.readline()
                self.privkey_hex = w.decode_hex(self.privkey_WIF)
                self.privkey_d = int(self.privkey_hex, 16)
                self.pubkey = w.pubkey_from_privkey(self.privkey_d, 0)
                self.addr = w.addr_from_privkey(self.privkey_d, 0)
                print('Private key (hex) is:\n ', self.privkey_hex)
                print('Private key (decimal) is:\n ', self.privkey_d)
                print('Private key (WIF) is:\n ', self.privkey_WIF)
                print('Public key (hex) is:\n ', self.pubkey)
                print('Pitcoin Address (b58check) is:\n ', self.addr)
                f = open('address', 'w')
                f.write(self.addr)
                f.close()
            except IOError:
                print("Error: can\'t find file or read data")
        else:
            print('Usage: import / path / to / file')
    
    def do_send(self, line):
        line = line.split()
        if len(line) == 2:
            try:
                f = open('address', 'r')
                self.addr = f.readline()
                tr = Transaction(self.addr, line[0], line[1])
                tr.singin(self.privkey_hex)
                trx = []
                trx.append(tr.amount)
                trx.append(tr.sender)
                trx.append(tr.recipient)
                trx.append(self.pubkey[2:])
                trx.append(tr.sig)
                tr.ser = Serializer(tr).ser
                print(tr.ser)
            except IOError:
                print("Error: can\'t find file \'address\' or read data")
        else:
            print('Usage: send <% Recipient Address%>, <% Amount%>')

    def do_balance(self, line):
        return

    def do_broadcast(self, line):
        try:
            print(server.broadcast(line))
        except IndexError:
            print('Usage: broadcast <serialized transaction>')

    def do_mempool(self, line):
        print(show_mem())

    def do_getmem(self, line):
        print(get_from_mem())

    def do_EOF(self, line):
        return True

#to debug
    def do_A(self, line):
        self.do_import('privkey')

    def do_B(self, line):
        self.do_send('18B7K7Jnz9YeiPHKQq4ULKcrcQtQBcKUzq 1')
        

if __name__ == '__main__':
    Wallet().cmdloop()
