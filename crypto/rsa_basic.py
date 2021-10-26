from Crypto.Util.number import *

def egcd(a, b):
    x,y = 0, 1
    u,v = 1, 0

    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a = a,r
        x,y = u,v
        u,v = m,n
        gcd = b
    return gcd, x, y

def main():
    n = 0xacb93757a309b7822f7dd536acacf32f
    e = 65537
    c = 0x46754CA87B2FAAD575E66F7ACFA68D9B4BDFD702445FC616F3D1949ED7CC301538781D51F88A138746C90B37CE9008C322C1322712262518D782335F4B77AE67


