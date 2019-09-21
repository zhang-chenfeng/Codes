import sys
import queue
friend = [[], [6], [6], [6, 4, 5, 15], [6, 3, 5], [6, 3, 4], [2, 1, 4, 5, 3, 7], [6, 8], [7, 9], [8, 10, 12], [9, 11], [10, 12], [9, 13, 11], [15, 12, 14], [13], [3, 13], [17, 18], [16, 18], [16, 17], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

q = queue.Queue()


def find(f1, f2):
    visited = []
    for f in friend[f1]:
        q.put(f)
        visited.append(f)
    sep = 0
    while not q.empty():
        sep += 1
        i = q.qsize()
        for fffff in range(i):
            ff = q.get()
            if ff == f2:
                q.queue.clear()
                return sep
            for fff in friend[ff]:
                if fff not in visited:
                    q.put(fff)
                    visited.append(fff)
    q.queue.clear()
    return 0


fn = False
while not fn:
    command = input()
    if command == "i":
        f1 = int(input())
        f2 = int(input())
        if f1 not in friend[f2]:
            friend[f2].append(f1)
        if f2 not in friend[f1]:
            friend[f1].append(f2)
    elif command == "d":
        f1 = int(input())
        f2 = int(input())
        friend[f1].remove(f2)
        friend[f2].remove(f1)
    elif command == "n":
        f1 = int(input())
        print(len(friend[f1]))
    elif command == "f":
        f1 = int(input())
        fof = {55}
        for f in friend[f1]:
            for ff in friend[f]:
                if ff != f1 and ff not in friend[f1]:
                    fof.add(ff)
        print(len(fof) - 1)
    elif command == "s":
        f1 = int(input())
        f2 = int(input())
        c = find(f1, f2)
        if c == 0:
            print("Not connected")
        else:
            print(c)
    elif command == "q":
        fn = True
