import numpy as np
def levenshteinDistance(str1, str2):
    l1, l2 = len(str1), len(str2)
    sol = np.zeros([l1+1, l2+1], dtype=np.int32)
    sol[1:, 0] = np.arange(1, l1+1)
    sol[0, 1:] = np.arange(1, l2+1)
    for i in range(1, l1+1):
        for j in range(1, l2+1):
           v = str1[i-1] != str2[j-1]
           sol[i, j] = min(sol[i-1,j]+1, sol[i,j-1]+1, sol[i-1,j-1]+v)
    return sol[-1, -1] 

print(levenshteinDistance("hello", "helleeee"))
