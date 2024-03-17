def compute(pat):
    lps = [0] * len(pat)
    len_ = 0
    i = 1
    while i < len(pat):
        if pat[i] == pat[len_]:
            len_ += 1
            lps[i] = len_
            i += 1
        else:
            if len_ == 0:
                lps[i] = 0
                i += 1
            else:
                len_ = lps[len_ - 1]
    return lps

def kmp(txt, pat):
    N = len(txt)
    M = len(pat)
    lps = compute(pat)
    i,j = 0,0
    while N-i >= M-j:
        if txt[i] == pat[j]:
            i += 1
            j += 1
        if j == M:
            print(f"find pattern at {i-j}")
            j = lps[j-1]
        elif i < N and pat[j] != txt[i]:
            if j == 0:
                i = i + 1
            else:
                j = lps[j-1]
        
# pat = "AABAACAABAA"
txt = "AABAACAADAABAABA"
pat = "AABA"
# print(compute(pat))
kmp(txt, pat)
