import math
n = int(input())
k = int(input())
if k >= n:
    print(k - n)
else:
    c = k * math.floor(n / k)
    d = k * math.ceil(n / k)
    print(min(abs(n - c), abs(n - d)))
