string = "OfdlDSA|3tXb32~X3tX@sX`4tXtz"
data = []

for i in range(len(string)):
	data.append(chr(ord(string[i]) ^ 7))
print "".join(data)
