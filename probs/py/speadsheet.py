import sys
con = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}


def calc(x, y, iter):
    if values[x][y] != -1:
        return values[x][y]
    box = sheet[x][y]
    try:
        box = int(box)
        values[x][y] = box
        return box
    except ValueError:
        dep = box.split("+")
        s = 0
        for grid in dep:
            if iter > 1000:
                values[x][y] = "*"
                return "*"
            val = calc(con[grid[0]], int(grid[1]) - 1, iter + 1)
            if val == "*" or (con[grid[0]] == x and int(grid[1]) - 1 == y):
                values[x][y] = "*"
                return "*"
            s += val
        values[x][y] = s
        return s


sheet = []
values = [[-1 for i in range(9)] for j in range(10)]
for a in range(10):
    sheet.append(sys.stdin.readline().split())
for x in range(10):
    for y in range(9):
        calc(x, y, 1)
for x in range(10):
    print(" ".join(map(str, values[x])))