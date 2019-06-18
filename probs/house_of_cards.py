n, k = map(int, input().split())
num = list(map(int, input().split()))
num.sort()
last = -k
sum = 0
for a in num:
    if a - last >= k:
        sum += 1
        last = a
print(sum)
