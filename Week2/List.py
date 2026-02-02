thislist = list(("apple", "banana", "cherry")) # note the double round-brackets
print(thislist)

mylist = ["apple", "banana", "cherry"]
print(type(mylist))#what data type is in my list

"""
List is a collection which is ordered and changeable. Allows duplicate members.
Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
Dictionary is a collection which is ordered** and changeable. No duplicate members.
"""

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[1])
print(thislist[-1])
print(thislist[2:5])
print(thislist[:4])
print(thislist[2:])
print(thislist[-4:-1])

thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

#we can change element
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1] = "blackcurrant"
print(thislist)#output: ["apple", "blackcurrant", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)#output: ["apple", "blackcurrant", "watermelon", "orange", "kiwi", "mango"]
thislist.insert(2, "watermelon")
print(thislist)#output: ["apple", "banana", "watermelon" ,"cherry", "orange", "kiwi", "mango"]
thislist.append("orange")
print(thislist)#output : ["apple", "banana", "cherry", "orange", "kiwi", "mango", "orange"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)#output : ["apple", "banana", "cherry", "orange", "kiwi", "mango","mango", "pineapple", "papaya"]
thislist.remove("banana")
thislist.pop(1)
thislist.pop()
del thislist[0]
del thislist
thislist.clear()
[print(x) for x in thislist]#easiest way to print list
thislist.sort()
thislist.sort(reverse = True)
thislist.reverse()
def myfunc(n):
  return abs(n - 50)
thislist.sort(key = myfunc)
mylist = thislist.copy()
list1.extend(list2)
"""
append()	Adds an element at the end of the list
clear()	Removes all the elements from the list
copy()	Returns a copy of the list
count()	Returns the number of elements with the specified value
extend()	Add the elements of a list (or any iterable), to the end of the current list
index()	Returns the index of the first element with the specified value
insert()	Adds an element at the specified position
pop()	Removes the element at the specified position
remove()	Removes the item with the specified value
reverse()	Reverses the order of the list
sort()	Sorts the list
"""

