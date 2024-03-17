from PIL import Image
import numpy as np
from collections import Counter

word2code = {}
class Node:
    def __init__(self, symbol, freq) -> None:
        self.symbol = symbol
        self.freq = freq    # 出现频次
        self.code = None    # 编码
        self.left = None    # 左子树
        self.right = None   # 右子树
    
    def update(self):       # 对应子树赋值
        self.left.code = [0]
        self.right.code = [1]
        
    
class Stack:
    def __init__(self) -> None:
        self.stack = []     # 存储所有节点
    
    def insert_sorted(self, node:Node): # 插入已经排好序的
        self.stack.append(node)     

    def __len__(self):
        return len(self.stack)
    
    def __getitem__(self, index): 
        return self.stack[index]
    
    def insert(self, node: Node):   # 按照顺序插入
        i = 0
        for i in range(len(self.stack)):
            if self.stack[i].freq > node.freq:
                self.stack.insert(i, node)
                return
        self.stack.append(node)     # 最大的直接放在最后
        
    def update(self):               # 最小的两个节点出栈
        s1 = self.stack.pop(0)
        s2 = self.stack.pop(0)
        return s1, s2


def cal_symbol_freq(data):          # 计算每个符号的出现频次并排序
    symbol_freq = dict(Counter(data))
    symbol_freq = sorted(symbol_freq.items(), key=lambda s: s[1])
    nodes = Stack()
    for s in symbol_freq:
        nodes.insert_sorted(Node(s[0], s[1]))
    return nodes

def updateCode(tree: Node, code):   # 获得每个符号的编码
    global word2code
    if code != None:
        tree.code.extend(code)
    if tree.symbol != None:
        word2code[tree.symbol] = "".join(np.array(tree.code[::-1]).astype(str))
        return
    updateCode(tree.left, tree.code)
    updateCode(tree.right, tree.code)
    

def huffman(data):              # 霍夫曼编码
    symbol_freq = cal_symbol_freq(data)

    while len(symbol_freq) > 1:
        s1, s2 = symbol_freq.update()
        root = Node(None, freq=s1.freq+s2.freq)
        root.left = s1
        root.right = s2
        root.update()
        symbol_freq.insert(root)
    tree = symbol_freq[0]
    updateCode(tree, tree.code)
    return tree


if __name__ == "__main__":
    
    # image = Image.open("test1.png")
    # image = np.array(image)
    # single_image = np.ravel(image[:, :, 0])
    # code = huffman(single_image)
    # print(word2code)
    
    s = ['a'] * 31 + ['b'] * 16 + ['d'] * 8  + ['g'] * 4 + ['c'] * 10 + ['e'] * 11 + ['f'] * 20
    huffman(s)
    print(word2code)
