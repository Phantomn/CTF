string = "OfdlDSA|3tXb32~X3tX@sX`4tXtz"
data = []
v3 = 0

for i in range(30):
	for j in range(len(string)):
		data.append(chr(ord(string[j]) ^ i))
	print "Key : %d Flag : %s"%(i,"".join(data))
	data = []
