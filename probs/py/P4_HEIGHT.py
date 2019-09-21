from sys import stdin
n = int(stdin.readline())
c, dp = [], []
for a in range(n):
    c.append(int(stdin.readline()))
    dp.append(-1)


def mx(ind):
    less = []
    for prev in range(ind - 1, -1, -1):
        if c[prev] < c[ind]:
            if dp[prev] == -1:
                dp[prev] = mx(prev)
            less.append(dp[prev] + c[ind])
    if len(less) == 0:
        dp[ind] = c[ind]
        return c[ind]
    return max(less)


m = 0
for x in range(n - 1, -1, -1):
    sm = mx(x)
    if sm > m:
        m = sm
print(m)

