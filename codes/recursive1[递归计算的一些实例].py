import math
import time
def gcd(a, b):
    if a == 0:
        return b
    else:
        return gcd(b % a, a)
    
def mpower(b, n, m):
    if n == 0:
        return 1
    else:
        return b * mpower(b, n-1, m) % m

def mpowerbetter(b,n,m):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return (mpowerbetter(b, int(n/2), m) * mpowerbetter(b, int(n/2), m))% m
    else:
        return (((mpowerbetter(b, math.floor(n/2), m) *mpowerbetter(b, math.floor(n/2), m)  ) % m) * (b % m)) % m

print(gcd(5, 8))
print(mpower(11, 13, 129))
print(mpowerbetter(11, 13, 129))
print(f"{(11 ** 13) % 129}")
