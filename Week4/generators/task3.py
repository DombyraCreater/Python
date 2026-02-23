n = int(input())

def twelve(n):
    a = 0
    while a<=n:
        if a%12==0:
            yield a
            a+=1
        else:
            a+=1

ctr = twelve(n)
for i in ctr:
    print(i, end = ' ')