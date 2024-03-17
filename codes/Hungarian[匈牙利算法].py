def match(visit, p, i):
    for j in range(N):
        if (j in adj[i]) and not visit[j]:
            visit[j] = True
            if p[j]==-1 or (match(visit, p, p[j]) != -1):   
                # p[j]==-1表示j还未配对，match(visit, p, p[j]) != -1表示p[j]配对的男生还能找到别的配对
                p[j] = i    # 内部记录匹配
                return j
    return -1
def Hungarian():
    p = [-1]*N          # 女生与男生的配对,p[i]表示第i个女生配对男生的标号
    for i in range(M):  # 对于每个男生
        visit = [False] * N     # 被访问过的女生
        j = match(visit, p, i)
        if j != -1:
            p[j] = i        # 外部记录匹配
    return p

if __name__ == "__main__":
    M = 4   # boys
    N = 4   # girls
    adj = [[1,3],[1],[0,2],[3]] # 男生对女生的好感
    p = Hungarian()
    print(p)