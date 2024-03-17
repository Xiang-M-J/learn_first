import numpy as np
def lcs(str1, str2):
    M, N = len(str1), len(str2)
    sol = np.zeros([M+1, N+1], dtype=np.int32)
    Llen = 0             # 最长公共子序列长度
    Lend = 0             # 最长公共子序列的终点
    for i in range(1, M+1):
        for j in range(1, N+1):
            if str1[i-1] == str2[j-1]:
                sol[i,j] = sol[i-1,j-1] + 1
            else:
                sol[i,j] = 0
            if sol[i,j] > Llen:
                Llen = sol[i,j]
                Lend = i

    if Llen == 0:
        print("无最长公共子序列")
    else:
        lseq = ""
        while Llen > 0:
            lseq = str1[Lend-1] + lseq 
            Lend -= 1
            Llen -= 1
        print(lseq)

lcs("ABABC", "BABCA")
