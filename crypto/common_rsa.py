from Crypto.Util.number import inverse, long_to_bytes

def extended_gcd(a:int, b:int):
    s1, s2 = 1, 0
    t1, t2 = 0, 1

    while(b):

        q = a // b
        a, b = b, a%b
        s1, s2 = s2, s1 - q*s2
        t1, t2 = t2, t1 - q*t2
    return s1, t1

if __name__ == "__main__":
    N = 0x82DAFD211C2A71F5141D3421261F394E0C986427048280A07FECE1C094863647946DF5A9229B7FCC8585E55B1A18FFE7310BD15803D8D378ED66297765D2322D

    c1 = 0x39776f6d4f684775517462715637582f7a436b7244783244476e532f347a7a5732534c6d54514331647166532f4442574d765235746b6877683452782b675550

    c2 = 0x6a384d6d68492f6144746577704e48424d51786244654c313166767146374574644474367977496461797359344a3032385955456d4c4d376e5162436e526b31
    
    # gcd(e1, e2 == 1
    e1 = 0x263c
    e2 = 65537

    s, t = extended_gcd(e1, e2)

    c1 = inverse(c1, N)
    c1 = pow(c1, -s, N)
    c2 = pow(c2, t, N)
    p = str(long_to_bytes((c1 * c2) % N))[2:-1]
    print(p)
