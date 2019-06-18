class A(object):
    def __init__(self):
        print("Hello from A")


class B(A):
    def hi(self):
        print("Hello from B")


class C(B):
    def __init__(self):
        print("Hello from C")

c = C()
