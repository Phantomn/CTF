#!/usr/bin/python3
import codecs
import binascii
a = codecs.decode("7d54535b7567201e6f016b3903123b6054444e6d3706401f3a31171353125a5d78474c6f5502401f44164c33", "hex")
b = "HackCTF{"
def encrypt(flag, key):
	enc = ''
	for i in range(len(flag)):
		enc += chr(ord(key[i % len(key)]) ^ ord(flag[i]))
	return enc
enc = encrypt(a, b)
c = binascii.hexlify(enc.encode())
enc = encrypt(c, a)
