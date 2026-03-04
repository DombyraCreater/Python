x = int(input())
list1 = input().split()
list2 = input().split()
ziped = list(zip(list1,list2))
a = input()
found = False
pos = 0

for i in range(x):
    if a == ziped[i][0]:
        found = True
        pos = i
        break

if found == True:
    print(ziped[pos][1])
else:
    print("Not found")