string = "OO]oUU2U<sU2UsUsK"
v2 = 72
data = ''
for i in range(0, len(string)-1):
    for j in range(0x20, 0x7f):
	tmp = ((j + 12)*v2 + 17) % 70 + 48
	if chr(tmp) == string[i]:
	    v2 = tmp
	    data += chr(j)
            break
print data
