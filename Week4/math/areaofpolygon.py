import math

n = int(input())
le = int(input())
radius = 0

def rad(n,le):
    return le/(2*math.tan(math.pi/n))

def area(n,le,rad):
    print(0.5*(n*le*rad))

radius = rad(n,le)
area(n,le,radius)