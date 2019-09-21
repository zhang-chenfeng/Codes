import sys
n = int(sys.stdin.readline())
a = {}
for x in range(n):
    r = int(sys.stdin.readline())
    if r not in a:
        a[r] = 1
    else:
        a[r] += 1
m1 = 0
m2 = 0
max1 = []
max2 = []
for i in a:
    if a[i] > m1:
        max2 = max1[:]
        m2 = m1
        max1 = [i]
        m1 = a[i]
    elif a[i] == m1:
        max1.append(i)
    elif a[i] > m2:
        m2 = a[i]
        max2 = [i]
    elif a[i] == m2:
        max2.append(i)

if len(max1) > 1:
    print(max(max1) - min(max1))
else:
    c = max1[0]
    k = max(max2)
    j = min(max2)
    print(max((abs(c - k), abs(c - j))))
