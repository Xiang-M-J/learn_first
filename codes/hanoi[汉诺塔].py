
def hanoi(n, f, m,  t):    # f：起点 m：中间 t：终点
    if n == 1:
        print(f"{f} -> {t}")    
        return
    hanoi(n-1, f, t, m)     # 将n-1个盘子从A搬到C，中间用B作为中间节点
    print(f"{f} -> {t}")    # 将A中最后一个盘子放到B
    hanoi(n-1, m, f, t)     # 将放在C上的n-1个盘子搬到B上，A作为中间节点

if __name__ == "__main__":
    hanoi(3, 'A', 'C', 'B') # 'A' 借助'C' 将盘子转移到 'B' 
