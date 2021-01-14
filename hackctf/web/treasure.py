import requests

URL = "http://ctf.j0n9hyun.xyz:2025/?page="

for i in range(55555):
	response = requests.get(URL+str(i))
	print(URL,i)
	if "HackCTF{" in response.text:
		print(i)
		break
print("Flag URL is %s%d"%(URL, i))
