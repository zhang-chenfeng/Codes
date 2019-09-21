from sys import stdin
r, c = [int(i) for i in stdin.readline().split()]
dp = [[-1 for column in range(c)] for row in range(r)]
dp[0][0] = 1
k = int(stdin.readline())
for a in range(k):
    x, y = [int(i) for i in stdin.readline().split()]
    dp[x - 1][y - 1] = 0


def paths(x, y):
    if dp[x][y] != -1:
        return dp[x][y]
    else:
        if x == 0:
            dp[x][y] = paths(x, y - 1)
        elif y == 0:
            dp[x][y] = paths(x - 1, y)
        else:
            dp[x][y] = paths(x - 1, y) + paths(x, y - 1)
    return dp[x][y]


print(paths(r-1, c-1))
