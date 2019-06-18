import sys, queue
n, m = map(int, sys.stdin.readline().split())
c = [[0] for i in range(n + 1)]
for x in range(m):
    a, b = map(int, sys.stdin.readline().split())
    c[a].append(b)
p, q = map(int, sys.stdin.readline().split())


def bfs(s1, s2):
    q = queue.Queue()
    for d in c[s1][1:]:
        if d == s2:
            return True
        c[d][0] = 1
        q.put(d)
    while not q.empty():
        person = q.get()
        for p in c[person][1:]:
            if p == s2:
                return True
            if c[p][0] == 0:
                c[p][0] = 1
                q.put(p)
    return False


if bfs(p, q):
    print("yes")
elif bfs(q, p):
    print("no")
else:
    print("unknown")
