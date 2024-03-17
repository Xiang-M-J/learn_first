
def searchb(x0, a ,d_r):
    for i in range(0, a):
        if (x0 * i + d_r) % a == 0:
            return i

def rev_replace(m, r):
    x = [m[0], r[0]]
    for i in range(1, len(m)):
        a = m[i]    # 由于m_j互素，所以a直接等于m[i]
        d_r = x[1] - r[i]
        b = searchb(x[0], a, d_r)
        x[1] += x[0] * b
        x[0] *= a
    return x[1]

if __name__ == "__main__":
    m = [99, 98, 97, 95]
    r = [65, 2, 51, 10]
    print(rev_replace(m, r))
    