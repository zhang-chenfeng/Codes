import queue

xp = ((0, 1), (1, 0), (0, -1), (-1, 0))
conveyor = {"U": 3, "D": 1, "L": 2, "R": 0}
n, m = [int(i) for i in input().split()]
f = []
p = []
ori = (0, 0)
cam = []
for x in range(n):
    f.append(input())
    p.append([])
    for y in range(m):
        c = f[x][y]
        if c == "W":
            p[x].append(0)
        else:
            p[x].append(-1)
        if c == "C":
            cam.append((x, y))
        if c == "S":
            ori = (x, y)
            p[ori[0]][ori[1]] = 0

seestart = False
for camera in cam:
    for di in xp:
        c = 1
        wall = False
        while not wall:
            node = (camera[0] + c * di[0], camera[1] + c * di[1])
            if f[node[0]][node[1]] == "W":
                wall = True
            elif f[node[0]][node[1]] == "S":
                seestart = True
            else:
                p[node[0]][node[1]] = 0
            c += 1

q = queue.Queue()
step = 0
for dire in xp:
    node = (ori[0]+dire[0], ori[1]+dire[1])
    letter = f[node[0]][node[1]]
    while letter in conveyor:
        p[node[0]][node[1]] = 0
        if p[node[0] + xp[conveyor[letter]][0]][node[1] + xp[conveyor[letter]][1]] != -1:
            break
        node = (node[0] + xp[conveyor[letter]][0], node[1] + xp[conveyor[letter]][1])
        letter = f[node[0]][node[1]]
    if f[node[0]][node[1]] == "." and p[node[0]][node[1]] == -1:
        p[node[0]][node[1]] = step
        q.put(node)
while not q.empty():
    step += 1
    nodes = q.qsize()
    for a in range(nodes):
        node = q.get()
        p[node[0]][node[1]] = step
        for dire in xp:
            new = (node[0]+dire[0], node[1]+dire[1])
            letter = f[new[0]][new[1]]
            while letter in conveyor:
                p[new[0]][new[1]] = 0
                if p[new[0] + xp[conveyor[letter]][0]][new[1] + xp[conveyor[letter]][1]] != -1:
                    break
                new = (new[0] + xp[conveyor[letter]][0], new[1] + xp[conveyor[letter]][1])
                letter = f[new[0]][new[1]]
            if letter == "." and p[new[0]][new[1]] == -1:
                p[new[0]][new[1]] = step
                q.put(new)

if seestart:
    for a in range(n):
        for b in range(m):
            if f[a][b] == ".":
                print(-1)

else:
    for a in range(n):
        for b in range(m):
            if f[a][b] == ".":
                if p[a][b] == 0:
                    print(-1)
                else:
                    print(p[a][b])
