#!/usr/bin/env python3
from string import ascii_letters
from random import randint, choice
from signal import alarm
from math import factorial
import native

OPCODE = {i: op for i, op in enumerate(
    ['Illl', 'IIll', 'IIIl', 'lIIl', 'IlIl',
     'lIll', 'lIII', 'llII', 'lllI', 'llll',
     'IllI', 'lIlI', 'llIl', 'IlII'])}

class TPU:
    def run(e, b, a=[]):
        alarm(5)
        e.i = 0
        e.c = 0
        e.r = [0] * 8
        e.a = bytes(a)
        e.o = []
        e.m = bytearray(8)
        e.b = bytes.fromhex(b)
        e.h = len(e.b)
        e.z = True
        while e.i != e.h:
            getattr(e, OPCODE[e.b[e.i]])()
            e.i += 1
            e.c += 1
        alarm(0)
        return e.o

    def e(e):
        e.i += 1
        return e.b[e.i]

    def Illl(e):
        e.r[e.e()] = e.e()

    def IIll(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] + e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.IIll(e.r[e.e()], e.r[e.e()])

    def IIIl(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] - e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.IIIl(e.r[e.e()], e.r[e.e()])

    def lIIl(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] & e.r[e.e()]
        else:
            e.r[e.e()] = native.lIIl(e.r[e.e()], e.r[e.e()])

    def IlIl(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] | e.r[e.e()]
        else:
            e.r[e.e()] = native.IlIl(e.r[e.e()], e.r[e.e()])

    def lIll(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] ^ e.r[e.e()]
        else:
            e.r[e.e()] = native.lIll(e.r[e.e()], e.r[e.e()])

    def lIII(e):
        i = e.e()
        e.r[i] = -e.r[i]

    def llII(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] >> e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.llII(e.r[e.e()], e.r[e.e()])

    def lllI(e):
        if e.z:
            e.r[e.e()] = e.r[e.e()] << e.r[e.e()] & 0xFF
        else:
            e.r[e.e()] = native.lllI(e.r[e.e()], e.r[e.e()])

    def llll(e):
        m = e.e()
        s = e.e()
        d = e.e()
        if e.z:
            if m == 0:e.r[d] = e.a[s]
            if m == 1:e.r[d] = e.m[s]
            if m == 2:e.r[e.r[d]] = e.m[s]
            if m == 3:e.r[d] = e.m[e.r[s]]
            if m == 4:e.m[d] = e.r[s]
            if m == 5:e.m[e.r[d]] = e.r[s]
            if m == 6:e.m[d] = e.r[e.m[s]]
        else:
            native.llll(e, m, s, d)

    def IllI(e):
        e.i = e.r[e.e()] - 1

    def lIlI(e):
        if e.r[e.e()]:e.e()
        else:e.i = e.r[e.e()] - 1

    def llIl(e):
        e.o.append(e.r[e.e()])
        e.c = 0

    def IlII(e):
        e.z ^= True

tpu = TPU()

code = input('chall 1 : ')
for i in range(20):
    a = randint(0, 100)
    b = randint(0, 100)
    assert a + b == tpu.run(code, [a, b])[0]

code = input('chall 2 : ')
for i in range(20):
    word = ''.join(choice(ascii_letters) for _ in range(7))
    assert word.swapcase() == ''.join(chr(_) for _ in tpu.run(code, word.encode()))

code = input('chall 3 : ')
for i in range(20):
    a = randint(0, 15)
    b = randint(0, 15)
    assert a * b == tpu.run(code, [a, b])[0]

code = input('chall 4 : ')
args = []
total = 0
for i in range(10):
    args.append(randint(0, 10))
    if total % 2:
        total = total + factorial(args[-1]) & 0xff
    else:
        total = total + sum(range(args[-1] + 1)) & 0xff
result = tpu.run(code, args)
if total == result[0]:
    print('good job. now, you can do anything!')
else:
    print('try harder!')
    exit(0)

while True:
    code = input('code : ')
    print(tpu.run(code))
