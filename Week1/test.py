n = int(input())
numbers = list(map(int, input().split()))
numbers.sort(reverse=True)
for i in range(n):
    print(numbers[i], end = ' ')
