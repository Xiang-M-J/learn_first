def next_permutation(perm):
    n = len(perm) - 1
    j = n - 1
    while perm[j] > perm[j+1]:
        j -= 1      # j是使得perm[j]<perm[j+1]的最大下标
    k = n
    while perm[j] > perm[k]:
        k -= 1      # perm[k]是在perm[j]右边大于perm[j]的最小整数
    perm[j], perm[k] = perm[k], perm[j]
    r = n
    s = j + 1
    while r > s:    # 把在第j位后边的排列尾部按递增顺序放置
        perm[r], perm[s] = perm[s], perm[r]
        r -= 1
        s += 1
    return perm

def factorial(n):
    s = 1
    for i in range(2, n+1):
        s *= i
    return s

def gen_permutation(N):
    perm = [i for i in range(1, N+1)]
    count = 1
    max_num = factorial(N)
    perms = [perm.copy()]       # 记得加上copy()，否则全部都会被修改
    while count < max_num:
        perm = next_permutation(perm)
        perms.append(perm.copy())
        count += 1
    return perms

if __name__ == "__main__":
    perms = gen_permutation(4)
    print(perms)
