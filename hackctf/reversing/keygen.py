enc = "OO]oUU2U<sU2UsUsK"
v2 = 72
data = [0]*65
flag = []
for i in range(len(enc)):
	for j in range(0x20, 0x7f):
		string  = ((ord(enc[i]) + 12) * v2 + 17) % 70 + 48
		v2 = string
