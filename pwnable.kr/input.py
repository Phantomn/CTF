from pwn import *
import os

# stage 1
argv = [str(i) for i in range(100)]
argv[ord('A')]="\x00"
argv[ord('B')]="\x20\x0a\x0d"
# stage 2
#stdin \x00\x0a\x00\xff
#stderr \x00\x0a\x02\xff
with open("./stderr", "w") as data:
    data.write("\x00\x0a\x02\xff")

# stage 3 env(\xde\xad\xbe\xef) = "\xca\xfe\xba\xbe"
env = {"\xde\xad\xbe\xef":"\xca\xfe\xba\xbe"}

# stage 4 open \x0a
with open("\x0a", "w") as data:
    data.write("\x00\x00\x00\x00")

# stage 5 send "\xde\xad\xbe\xef" port argv['C']
argv[ord('C')]='55555'

p = process(executable="./input", argv=argv, stderr=open("./stderr"),env=env)
p.sendline("\x00\x0a\x00\xff")
p = remote("localhost", 55555)
p.send("\xde\xad\xbe\xef")
p.interactive()
