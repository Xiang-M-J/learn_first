def partition1(num, n, loc, sum, sol:list):
    if sum == n:
        # print(sol[:loc])
        return
    if sum > n:
        return 
    for i in range(num, n+1):
        sol[loc] = i
        partition1(i, n, loc+1, sum+i, sol)

def partition2(num, n, loc, sum, sol:list):
    """
    num: 当前分解因子   n: 需要分解的整数
    loc: 分解因子的序号 sum: 总和
    sol: 存放分解因子
    """
    if sum == n:
        print(sol[:loc])
        return
    for i in range(num, n+1-sum):  # 剪去一些不可能的分支
        sol[loc] = i
        partition2(i, n, loc+1, sum+i, sol)

N = 8
sol = [0]*N
partition2(1, N, 0, 0, sol)
