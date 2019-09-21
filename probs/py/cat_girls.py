import sys
n, cam = map(int, sys.stdin.readline().split())
nekos = [() for i in range(cam)] # ind 0 = max cuteness; 1 = max_pose 2 = pose
last_neko = 0
cam_left = 0
cam_right = 0
for event in range(n):
    e = sys.stdin.readline()
    if e == "D":
        if cam_right == last_neko:
            cam_right -= 1
        last_neko -= 1
    else:
        neko_width, cuteness = map(int, e.split()[1:])




