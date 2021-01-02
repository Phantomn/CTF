string = "H`cjCUFzhdy^stcbers^D1_x0t_jn1w^r2vdrre^3o9hndes1o9>}"
data = ""
for i in range(len(string)):
	data += chr(ord(string[i]) ^ (i % 2))

print data
