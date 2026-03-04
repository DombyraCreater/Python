from functools import reduce

list1 = list(map(int,input().split()))
strings = input().split()
nums = list()

def sqr(x):
    return x*x

def is_even(x):
  return x % 2 == 0

list2 = list(map(sqr,list1))
result = list(filter(is_even,list2))
print(result)

sum_lambda = reduce(lambda x, y: x + y, result)
print(f"Sum with lambda: {sum_lambda}")

for i, strs in enumerate(strings):
    nums.append(i+1)

zipped_data = list(zip(nums, strings))
print(zipped_data)

print(isinstance(nums, int))
new_nums = list(map(int,nums))
print(all(isinstance(x, int) for x in new_nums))
