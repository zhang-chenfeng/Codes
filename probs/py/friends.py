from sys import stdin
n = int(stdin.readline())
friends = {}
for x in range(n):
    a, b = map(int, stdin.readline().split())
    friends[a] = b


def search(s, f):
    sep = 0
    place = s
    while sep < n:
        if friends[place] == f:
            return "Yes " + str(sep)
        place = friends[place]
        sep += 1
    return "No"


c, d = map(int, stdin.readline().split())
while c != 0 and d != 0:
    print(search(c, d))
    c, d = map(int, stdin.readline().split())
