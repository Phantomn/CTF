from pwn import *
string = "OO]oUU2U<sU2UsUsK"
v2 = 72
data = ''
for i in range(0, len(string)):
    for j in range(0x20, 0x7f):
        k = ((j + 12) * v2 + 17) % 70 + 48
        if string[i] == chr(k):
            v2 = k
            data += chr(j)
            break
r = remote("ctf.j0n9hyun.xyz", 9004)
print r.recvline()
r.sendline(data)
print r.recvuntil("\n")
print r.recvuntil("\n")
