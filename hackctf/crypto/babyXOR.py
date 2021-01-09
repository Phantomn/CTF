enc = "7d54535b7567201e6f016b3903123b6054444e6d3706401f3a31171353125a5d78474c6f5502401f44164c33".decode("hex")
flag = "HackCTF{"

key = ''
for i in range(len(flag)):
	key += chr(ord(enc[i]) ^ ord(flag[i]))

flag = ''
for i in range(len(enc)):
	flag += chr(ord(enc[i]) ^ ord(key[i % len(key)]))
print flag
