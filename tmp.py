def lin_search(int_list, key):
    tmp = len(int_list) - 1
    if tmp == -1 or int_list[tmp] == key:
        return tmp
    return lin_search(int_list[:tmp], key)


def f2b(int_list, key):
    if len(int_list) == 0:
        return -1
    if int_list[0] == key:
        return 0
    r = f2b(int_list[1:], key)
    return r + (0 if r == -1 else 1)


l = [1, 2, 3, 4, 5, 6]

print(lin_search(l, 4))
print(lin_search(l, 6))
print(lin_search(l, 7))

print(f2b(l, 4))
print(f2b(l, 6))
print(f2b(l, 7))

def linear_search():
    def search():
        if():
            if ():
                return 1
            else:
                return 2

        else:
            return 1 + search(i, k)
        
    result = search()






    
