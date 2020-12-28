import hashlib, random, string

arr = {}

find_hash = '0000'

for i in range(1000000000):
    randomstr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
    sha1value = hashlib.sha256(randomstr.encode('utf-8'))
    # arr[sha1value.hexdigest()[:16]] = randomstr
    if (find_hash in sha1value.hexdigest()[:4]):
        print(randomstr)
        print(sha1value)
        exit(0)

    if (find_hash == sha1value.hexdigest()[:4]):
        print(randomstr)
        print(sha1value)
        exit(0)
    print(randomstr, " ", sha1value.hexdigest())
