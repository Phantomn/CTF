enc = "OO]oUU2U<sU2UsUsK"
v2 = 72
flag = ''

for i in range(len(enc)):
	for j in range(0x21, 0x7f):
		tmp = ((j + 12) * v2 + 17) % 70 + 48
		if chr(tmp) == enc[i]:
			v2 = tmp
			flag += chr(j)
			break
print flag
