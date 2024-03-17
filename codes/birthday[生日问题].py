import random
n=23
days = 366
N = 10000
birthday = []
count = 0
for _ in range(N):
    for _ in range(n):
        now = random.randint(1, 366)
        if now in birthday:
            count += 1
            birthday = []
            break
        else:
            birthday.append(now)
    birthday = []


def cal(days, n):
    p = 1
    for i in range(n):          # p_n = N! / ((N-n)!*366^n)
        p *= ((days - i)/366) 
    return 1- p

print(cal(days, n))

print(count / N)

