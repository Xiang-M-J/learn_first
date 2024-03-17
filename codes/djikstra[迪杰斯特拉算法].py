# https://zhuanlan.zhihu.com/p/63395403
import numpy as np


class Net:
    def __init__(self, data, length, inf) -> None:
        self.net = np.zeros([length, length])
        self.length = length
        for edge in data:
            n1, n2, distance = edge
            ind1, ind2 = ord(n1) - 65, ord(n2) - 65
            self.net[ind1, ind2] = self.net[ind2, ind1] = distance
        self.net[np.where(self.net==0)] = inf
        for i in range(length):
            self.net[i,i] = 0
            

def Djikstra(start: int, graph:np.array):
    S = [start]     # 已经遍历过的节点
    U = [x for x in range(len(graph))]    # 未遍历过的节点
    U.remove(start)
    distance = graph[start]               # 起点到其它点的距离
    
    while len(U):
        idx = U[0]
        for i in U:                         # 找到U中距离最小的点
            if distance[i] < distance[idx]: 
                idx = i
        
        S.append(idx)
        U.remove(idx)

        for i in U:                         # 更新U中点的距离
            distance[i] = min(distance[idx] + graph[idx][i], distance[i])

    return distance

# 返回起点到各个终点的路径和距离
def Djikstra2(start: int, graph: np.array) -> list:
    S = [start]
    U = [x for x in range(len(graph))]    # 未遍历过的节点
    U.remove(start)

    distance = graph[start]

    # 创建字典 为直接与start节点相邻的节点初始化路径
    path = {}
    for i in range(len(distance)):
        # if i != start:
        path[i] = [start]

    while len(U):
        idx = U[0]
        for i in U:
            if distance[i] < distance[idx]: idx = i

        U.remove(idx)
        S.append(idx)

        for i in U:         # 更新距离和路径
            if distance[idx] + graph[idx][i] < distance[i]:
                distance[i] = distance[idx] + graph[idx][i]
                path[i] = path[idx] + [idx]

    return distance, path

# 返回起点到目标终点的路径和距离
def Djikstra3(start: int, end: int, graph: np.array) -> list:
    S = [start]
    U = [x for x in range(len(graph))]    # 未遍历过的节点
    U.remove(start)

    distance = graph[start]

    # 创建字典 为直接与start节点相邻的节点初始化路径
    path = {}
    for i in range(len(distance)):
        path[i] = [start]

    while len(U):
        idx = U[0]
        for i in U:
            if distance[i] < distance[idx]: idx = i

        U.remove(idx)
        S.append(idx)

        for i in U:
            if distance[idx] + graph[idx][i] < distance[i]:
                distance[i] = distance[idx] + graph[idx][i]
                path[i] = path[idx] + [idx]
        if idx == end:
            break
    return distance[idx], path[idx], end

def print_path(distance, path):
    if len(distance) != len(path):
        print("距离集合大小与路径集合大小不匹配")
        return
    length = len(distance)
    end_points = list(path)
    for i in range(length):
        end_p = end_points[i]
        for j in range(len(path[end_p])):
            print(chr(path[end_p][j]+65), end='\t')
            # print(chr())
        print(chr(end_p+65), end='\t')
        print(distance[i])
        # print("")

def print_single_path(distance, end, path):
    
    for j in range(len(path)):
        print(chr(path[j]+65), end='\t')
    print(chr(end+65), end='\t')
    print(distance)

if __name__ == "__main__":
    inf = 1000
    data = [('A', 'B', 12), ('B', 'C', 10), ('C', 'D', 3), ('A', 'F', 16), ('A', 'G', 14), ('B', 'F', 7),
            ('G', 'F', 9), ('G', 'E', 8), ('F', 'E', 2), ('F', 'C', 6), ('C', 'E', 5), ('E', 'D', 4)]
    net = Net(data, length=7, inf=inf)
    graph = net.net

    # distance = Djikstra(0, graph)
    # print(distance)

    distance, path = Djikstra2(0, graph)
    print_path(distance, path)

    # distance, path, end = Djikstra3(0, 3, graph)
    # print_single_path(distance, end, path)
