def fastexponent(b, n, m):
    x = 1
    power = b % m
    for i in range(len(n)):
        if n[i] ==1 :
            x = x*power % m
        power = power * power % m
    return x

def Dec2bin(number):
    s = []
    while number > 0:
        rem = number % 2
        s.append(rem)
        number = number // 2
    return s

b = 2182
n_ = 937
m = 2537
n = Dec2bin(n_)
print(fastexponent(b, n, m))  # 计算 b^n mod m
