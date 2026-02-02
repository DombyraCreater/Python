tuple1 = ("abc", 34, True, 40, "male")
print(thistuple[1])
print(thistuple[-1])
print(thistuple[2:5])
print(thistuple[:4])
print(thistuple[2:])
print(thistuple[-4:-1])
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)

""""""

fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow)
print(red)

for i in range(len(thistuple)):
  print(thistuple[i])

fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)

"""
count()	Returns the number of times a specified value occurs in a tuple
index()	Searches the tuple for a specified value and returns the position of where it was found
"""
