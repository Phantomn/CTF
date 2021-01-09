def gcd(a, b):
	while b != 0:
		a, b = b, a%b
	return a
def decrypt(pk, text):
	key, n = pk
	plain = [chr((char ** key) % n) for char in text]
	return ''.join(plain)
def encrypt(pk, plain):
	key, n = pk
	cipher = [ord(char) ** key % n for char in plain]
	return cipher
def get_private_key(e, tot):
	k = 1
	while (e*k)%tot != 1 or k == e:
		k += 1
	return k
def get_public_key(tot):
	e = 2
	while e<tot and gcd(e, tot) != 1:
		e += 1
	return e
def main():
	m = 0x4730dcb8284416e44265091248de1ba51ce685ae5ff1276e263f72a1c90e34bcddc0ad1aa7757f1130c2f497b0629fb620e63b0b613ebe82c8b0a8d6f91a6652947f25c026307446cb7552e075e4754f1d60685a2b45e6238d3aca9934e47c0447e06d6162c91f912d14fb262ffce00e59fc8d04cbeb86cc5f087fbfe620b10e4d6a2c7ca9cb2ed315c31ee07b994b38c2827308c82de3b9ca7352505fe9b10a0ab4c81acc8334587f1277647509dca65001ad418f71e537d32bd71c10c89966b91a9426b440f3db5c52d4faf7440fbdae309bdd70769198e64995a6b3fdae748cc5db22dff8aa4fb235af657c96390d923a2b216dc34c07e28c588d8ef7c882

	p = 165500656692790480820099871308511495889550056248884963056391533737398719640777027536552348753003910353538512236389328276408434154714592616388810121411482595574799223632695324557638432891315001647024573557093357114908462069403023829967780936191142143068307535312844772151507357729244716123687935330409738850181
	q = 122141438575770439104084639124669389798489623069980415671656975299923395151301777382093192959734330849008684250930530493655750402979451442939127736597078242925067195617957339753271262399847630938612930834827285581446954616798548644945058711157525778059878711651283927027641401287892466364366504983328484106481
	print "Two Prime Numbers(p and q) are : %s and %s"%(str(p),str(q))
	n = p*q
	print "n(p*q)=%s * %s = %s"%(str(p),str(q),str(n))

	totient = (p-1)*(q-1)
	print "(p-1)*(q-1)=%s"%(str(totient))

	e = 65537
	print "Public Key(n, e) : (%s, %s)"%(str(n),str(e))

	d = get_private_key(e, totient)
	print "Private Key(n, d) : (%s, %s)"%(str(n),str(d))

	encrypted_msg = encrypt((e,n),m)
	print "Encrypted Message : %s"%(''.join(map(lambda x: str(x), encrypted_msg)))

	print "Decrypted Message : %s"%(decrypt((d,n), encrypted_msg))

if __name__ == '__main__':
	main()

