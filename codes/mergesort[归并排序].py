import math
def mergesort(L):
    n = len(L)
    if n > 1:
        m = math.floor(n / 2)
        L1 = L[:m]
        L2 = L[m:]
        L = merge(mergesort(L1), mergesort(L2))
    return L
    
def merge(L1:list, L2:list):
    L = []
    while len(L1) > 0 and len(L2) > 0:
        if L1[0] < L2[0]:
            L.append(L1.pop(0))
        else:
            L.append(L2.pop(0))
        if len(L1) == 0:
            L.extend(L2)
            L2.clear()
            break
        if len(L2) == 0:
            L.extend(L1)
            L1.clear()
            break
    return L
        
print(mergesort([8, 2, 4, 6, 9, 7, 10, 1, 5, 3, 2]))
