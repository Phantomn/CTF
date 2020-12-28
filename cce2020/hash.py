import random
import sys
import hashlib

class letter:
    ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+,./:;\"\'`[]\{\}\\|<>~"
    digits = "1234567890"

string = letter()
head=b"CCE2020_"
while True:
    for i in range(0x20, 0x7f):
        randstr=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(4))
        encoded_string = head+randstr.encode()
        hexdigest = hashlib.sha256(encoded_string).hexdigest()
        if hexdigest == "03849e08b5049e1bb4f75df3925df6d212a74276aad66820130095476dd946db":
            print("[+] encoded_string : %s"%encoded_string)
            print("[+] hexdigest %s"%hexdigest)
            sys.exit(0)
