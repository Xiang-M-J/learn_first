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

def ex_euclid(a, b):
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
    print(f"s = {s}, t = {t}")
    print(f"{x} == {s * a + t * b} ")

ex_euclid(252, 198)
