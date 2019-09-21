import sys
n = int(sys.stdin.readline())
m = {}
for x in range(n):
    chem = sys.stdin.readline()
    m[chem] = []
t = int(sys.stdin.readline())
for i in range(t):
    pr = sys.stdin.readline()
    m[pr].append(i + 1)
for e in m:
    for a in m[e]:
        print(a)


def prime(n):
    import math
    for i in range(1, int(math.sqrt(n))):
        if n % i == 0:
            return False
    return True
