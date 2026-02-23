import math

n = int(input())

def rad(n):
    return n*((math.pi)/180)

res = rad(n)
print(f"{res:.6f}")