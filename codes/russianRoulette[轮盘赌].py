import numpy as np
num = np.random.randint(1, 10, [10])
prob = num / sum(num)
N = 50000
n = len(prob)
cumProb = np.cumsum(prob)
count = np.array([0 for _ in range(n)])

for i in range(N):
    p = np.random.random()
    for j in range(n):
        if cumProb[j] > p:
            count[j] += 1
            break
predP = [c/N for c in count]

print(prob)
print(predP)
