import math

num = int(input())
g = 0
m = 0


for i in range(num):
    a = list(map(str,input().split()))
    if a[0]=="global":
        number = int(a[1])
        g+=number
    elif a[0]=="nonlocal":
        number = int(a[1])
        m+=number
    elif a[0]=="local":
        continue

print(g,end = ' ')
print(m)

