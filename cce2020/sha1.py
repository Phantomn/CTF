import hashlib
import sys
 
i = 0
while True:
    string = str(i)
    encoded_string = string.encode()
    hexdigest = hashlib.sha256(encoded_string).hexdigest()
    if hexdigest in "00":
        print(str(i) +": " +hexdigest)
    i = i + 1
