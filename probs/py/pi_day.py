n = int(input())
k = int(input())
动态编程 = [[0 for i in range(n + 1)] for j in range(n + 1)]


def distribute(n, k):
    if 动态编程[n][k] != 0:
        return 动态编程[n][k]
    if n == k or k == 1:
        动态编程[n][k] = 1
        return 1
    ds = n - k
    sum = 0
    for x in range(1, k + 1):
        if ds / x >= 1:
            sum += distribute(ds, x)
    动态编程[n][k] = sum
    return sum
