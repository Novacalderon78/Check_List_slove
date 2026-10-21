def linespace(n):
    print(" " * n, end="")

def lineharp(n):
    print("#" * n, end="")

def baseline(space, sharp):
    linespace(space)
    lineharp(sharp)
    print()

def top_leaf():
    baseline(4, 1)
    baseline(3, 3)
    baseline(2, 5)

def bottom_leaf():
    baseline(3, 3)
    baseline(2, 5)
    baseline(0, 9)

def trunk():
    baseline(3, 3)
    baseline(3, 3)
    baseline(3, 3)

def tree():
    top_leaf()
    bottom_leaf()
    trunk()

tree()