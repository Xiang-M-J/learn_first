import numpy as np

coins = np.array([[5,5], [9, 1], [8, 2], [4, 6], [7, 3]])   
# 两种硬币A、B扔出来的结果，如[9，1]代表抛出9次正面，1次反面，每一轮只会选择一种硬币抛出，试估计两种硬币抛出正面的概率

# 初始化为0.5
thetaA = 0.6
thetaB = 0.5

N = coins.shape[0]
T = 100     # 迭代次数

iter_coin = np.array([[0., 0., 0., 0.] for _ in range(N)])

for t in range(T):
    for i in range(N):      # E步，估计隐藏变量的分布
        pA = thetaA ** coins[i, 0] * (1-thetaA) ** coins[i, 1]    # 使用硬币A的概率
        pB = thetaB ** coins[i, 0] * (1-thetaB) ** coins[i, 1]    # 使用硬币B的概率
        iter_coin[i, 0] = pA / (pA + pB) * coins[i, 0]  # 使用硬币A抛出正面的次数
        iter_coin[i, 1] = pA / (pA + pB) * coins[i, 1]  # 使用硬币A抛出反面的次数
        iter_coin[i, 2] = pB / (pA + pB) * coins[i, 0]
        iter_coin[i, 3] = pB / (pA + pB) * coins[i, 1]
        
    thetaA = sum(iter_coin[:, 0]) / sum(sum(iter_coin[:, :2]))  #  M步，重新估计参数
    thetaB = sum(iter_coin[:, 2]) / sum(sum(iter_coin[:, 2:]))

print(thetaA, thetaB)

# 假设男女身高服从正态分布，均值和标准差如下，暂时无法得到好的结果
meanM, deltaM = 172.3, 8.2
meanF, deltaF = 165.4, 7.6
male = np.random.normal(meanM, deltaM, size=[50])
female = np.random.normal(meanF, deltaF, size=[50])

data = np.r_[male, female]
np.random.shuffle(data)

# 初始化均值和标准差
meanMP, deltaMP = 170, 10
meanFP, deltaFP = 160, 10

record = []
maleP = []
femaleP = []
for t in range(T):
    for p in data:
        pM = (p - meanMP) / deltaMP
        pF = (p - meanFP) / deltaFP
        record.append(abs(pM)/abs(pF))
        if abs(pM) > abs(pF):
            femaleP.append(p)
        else:
            maleP.append(p)
    # record = (record - np.mean(record)) / np.std(record)
    # idx = np.argsort(record)
    # femaleP = data[idx[:50]]
    # maleP = data[idx[50:]]
    # if len(maleP) > len(femaleP):
    #     # maleP.sort(reverse=True)
    #     femaleP.extend(maleP[100:])
    #     maleP = maleP[:100]
    # elif len(maleP) < len(femaleP):
    #     # femaleP.sort(reverse=True)
    #     maleP.extend(femaleP[100:])
    #     femaleP = femaleP[:100]
    meanMP = np.mean(maleP)
    deltaMP = np.std(maleP)
    meanFP = np.mean(femaleP)
    deltaFP = np.std(femaleP)
    record = []
    # print(len(maleP))
    # print(len(femaleP))
    maleP = []
    femaleP = []

print(meanMP, deltaMP)
print(meanFP, deltaFP)
