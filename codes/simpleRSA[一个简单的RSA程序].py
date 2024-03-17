def Euclid(a, b):
    x = a
    y = b
    qs = []
    while y != 0:
        r = x % y
        qs.append( x // y)
        x = y
        y = r
    return x, qs

def ex_euclid(a, b):        # 扩展欧几里得算法求解贝组系数
    x, qs = Euclid(a, b)
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1
    for i in range(len(qs)-1):
        s = s0 - s1 * qs[i]
        t = t0 - t1 * qs[i]
        s0, s1 = s1, s
        t0, t1 = t1, t
    return s, t

def cal_d(p, q, e):
    s, _ = ex_euclid(e, (p-1)*(q-1))
    return s

def fastexponent(b, n, m):  # 快速模幂运算
    n = Dec2bin(n)
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

def encode(o_x, e, n):
    e_x = []
    for x in o_x:
        e_x.append(fastexponent(int(x), e, n))
    return e_x

def decode(e_x, d, n):
    d_x = []
    for x in e_x:
        d_x.append(str(fastexponent(x, d, n)).rjust(4, '0'))
    return d_x

def str2int(msg:str):  # 仅支持大写字母
    msg = msg.upper()
    x = []
    for m in msg:
        x.append(str(ord(m) - 65).rjust(2, '0'))
    # 因为 n = p*q = 2537，而 2525 < 2537 < 252525，所以分为4个字符一组，即两个字母一组
    x_ = []
    if len(x) % 2 != 0:
        x.append("00")
    for i in range(0, len(x), 2):
        x_.append(x[i] + x[i+1])
    return x_

def int2str(d_x):  # 仅支持大写字母
    msg = ""
    for x in d_x:
        x0 = x[:2]
        x1 = x[2:]
        msg += chr(int(x0)+65)
        msg += chr(int(x1)+65)
    return msg


if __name__ == "__main__":
    e = 13
    p = 43
    q = 59
    n = p * q
    d = cal_d(p, q, e)

    msg = "HELLOWORLD"
    x = str2int(msg)
    print(f"origin text: {x}")
    e_x = encode(x, e, n)
    print(f"encode text: {e_x}")
    d_x = decode(e_x, d, n)
    print(f"decode text: {d_x}")
    m = int2str(d_x)
    print(f"msg: {m}")




