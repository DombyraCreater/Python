n = int(input())
first = True

def even(n):
    a = 0
    while a<=n:
        yield a
        a+=2

ctr = even(n)
for i in ctr:
    if first == True:
        print(i,end = '')
        first = False
    else:
        print(f",{i}",end='')