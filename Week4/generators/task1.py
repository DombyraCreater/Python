n = int(input())

def sqr(n):
    a = 1
    while a<=n:
        yield a*a
        a+=1

ctr = sqr(n)
for i in ctr:
    print(i)