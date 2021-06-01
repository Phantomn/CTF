enc = "1617181926381617919194"[::-1]
key = ""
temp = ""

for i in range(22):
	temp = ord(enc[i])^0xc
	if i%2 == 0:
		temp -= 4
	else:
		temp += 4
	key += chr(temp)
print key