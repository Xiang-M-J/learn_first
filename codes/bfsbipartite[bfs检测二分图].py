def bfs(node):
    queue = []
    color[node] = 1
    queue.append(node)
    while len(queue) > 0:
        cur = queue.pop(0)
        edge = adj[cur]
        for i in range(len(edge)):
            v = edge[i]
            if color[v] == 0:
                color[v] = -color[cur]
                queue.insert(0, v)
            else:
                if color[v] == color[cur]:
                    return False
    return True
if __name__ == "__main__":
    adj = [[4,6],[4],[4,5],[6,7],[0,2],[2],[0,3],[3]]
    color = [0]*8
    print(bfs(1))
    print(color)
