import string

def sub_Encrypt(input, key):
	data = []
	
	for ch in input:
		if ch.isalpha():
			tmp = ch.lower()
			tmp = ord(tmp)
			tmp -= ord('a')
			tmp -= (key % 26)
			tmp = Alpha[tmp]
			
			if ch.islower():
				ch = tmp.lower()
			else:
				ch = tmp.upper()
		data.append(ch)
	return data

Alpha = list(string.ascii_lowercase)

try:
	message = input("Input Message >> ")
	for i in range(0, 26):
		key = i
		data = sub_Encrypt(message, key)
		print ("Key : %d String : %s"%(i,"".join(data)))
    		
except EOFError:
    print("EOFError occurred")

except ValueError:
    print("ValueError occurred")
