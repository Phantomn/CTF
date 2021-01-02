string = ""
with open("Cipher.txt", "rb") as f:
	string = f.read()
print string[::-1]
f.close()
