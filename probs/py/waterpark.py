import sys
n = int(sys.stdin.readline())
动态编程 = [[-1, 1] for i in range(n)]
x, y = map(int, sys.stdin.readline().split())
while x != 0 and y != 0:
    动态编程[y - 1].append(x - 1)
    动态编程[x - 1][1] = 0
    x, y = map(int, sys.stdin.readline().split())


def 方法(pt):
    if 动态编程[pt][0] != -1:
        return 动态编程[pt][0]
    if len(动态编程[pt]) == 2:
        if 动态编程[pt][1] == 1:
            return 0
        return 1
    sm = 0
    for prev in 动态编程[pt][2:]:
        sm += 方法(prev)
    动态编程[pt][0] = sm
    return sm


tsum = 0
for node in range(n):
    if 动态编程[node][1] == 1:
        tsum += 方法(node)
print(tsum)
