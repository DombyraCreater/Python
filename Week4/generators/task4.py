a = list(map(int,input().split()))

def square1(a,b):
    while a<=b:
        yield a*a
        a+=1
def square2(a,b):
    i = a
    for i in range(b+1):
        yield a*a
        a+=1
ctr = square1(a[0],a[1])
for i in ctr:
    print(i,end = ' ')
ctr = square2(a[0],a[1])
for i in ctr:
    print(i,end = ' ')