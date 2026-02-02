i = 1
while i < 6:
  print(i)
  i += 1

#break stop the while

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#continue statement we can stop the current iteration, and continue with the next:

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)


#we can add else to while
i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")