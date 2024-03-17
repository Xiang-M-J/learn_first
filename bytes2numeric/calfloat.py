import numpy as np
e = "10000000"
f = "10010010000111111011011"
e = list(e)
f = list(f)
e = np.array(e).astype(np.int32)
f = np.array(f).astype(np.int32)
def calf(f):
    temp = 0
    for i in range(len(f)):
        temp += f[i]*(2**(-i-1))
    return temp

def cale(e):
    temp = 0
    for i in range(len(e)):
        temp += e[i] * (2**(len(e)-i-1))
    return temp

def calfloat(e, f):
    return 2**(e-127) * (1+f)
print(cale(e))
print(calf(f))
print(calfloat(cale(e), calf(f)))