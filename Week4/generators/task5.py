n = int(input())

def ret(n):
    a = n
    while a>=0:
        yield a
        a-=1


ctr = ret(n)
for i in ctr:
    print(i, end = ' ')