from sys import stdin
di = ((0, 1), (1, 0), (0, -1), (-1, 0))


def go():
    n = int(stdin.readline())
    mountain = []
    visit = []
    for x in range(n):
        mountain.append([])
        visit.append([])
        for y in range(n):
            mountain[x].append(int(stdin.readline()))
            visit[x].append(0)
    result = dfs((0, 0), 0, mountain, mountain[0][0], n, visit)
    if result == 0:
        return "CANNOT MAKE THE TRIP"
    else:
        return result


def dfs(node, oxygen, mountain, oxy_a, side, visited):
    visited[node[0]][node[1]] = 1
    paths = []
    for x in range(4):
        inc = False
        next = (node[0] + di[x][0], node[1] + di[x][1])
        if 0 <= next[0] < side and 0 <= next[1] < side and visited[next[0]][next[1]] != 1:
            altnow = mountain[node[0]][node[1]]
            altnex = mountain[next[0]][next[1]]
            if abs(altnow - altnex) <= 2:
                if altnex > oxy_a or altnow > oxy_a:
                    inc = True
                if next[0] == next[1] == side - 1:
                    return oxygen + (1 if inc else 0)
                ne = dfs(next, oxygen + (1 if inc else 0), mountain, oxy_a, side, visited)
                if ne != 0:
                    return ne
    return 0


t = int(stdin.readline())
for trip in range(t):
    print(go())
    print()

