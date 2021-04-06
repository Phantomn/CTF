data = "YKTHZBH7XJTzSM5lZpH0S3G0FN0="
decrypt = ''

for i in range(len(data)):
    v1 = ord(data[i])
    v2 = v1 - 65
    if((v1 - 65) <= 0x19):
        if(v2 < 6):
            v2 += 26
        v1 = (v2 - 6) % 26 + 65
        data[i] += chr(v1)
    v3 = v1 - 97
    if(v3 <= 0x19):
        if(v3 < 6):
            v3 += 26
        data[i] += chr((v3 - 6) % 26 + 97)
print data
