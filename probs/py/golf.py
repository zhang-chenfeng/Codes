n = int(input())
c = int(input())
dp = [-1 for i in range(n + 1)]
clubs = []
for x in range(c):
    d = int(input())
    clubs.append(d)
    dp[d] = 1


def stroke(s):
    if dp[s] != -1:
        return dp[s]
    ans = []
    for club in clubs:
        if s - club >= 0:
            prev = stroke(s - club)
            if prev > 0:
                ans.append(stroke(s - club) + 1)
    if len(ans) == 0:
        dp[s] = 0
    else:
        dp[s] = min(ans)
    return dp[s]


fin = stroke(n)
if fin > 0:
    print(" ".join(("Roberta wins in", str(fin), "strokes.")))
else:
    print("Roberta acknowledges defeat.")
