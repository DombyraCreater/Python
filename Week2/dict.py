thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"],
  "model": "Mustang"
}

x = thisdict["model"]
x = thisdict.get("model")
x = thisdict.keys()
x = thisdict.values()
x = thisdict.items()
if "model" in thisdict:
  print("Yes, 'model' is one of the keys in the thisdict dictionary")
thisdict.update({"year": 2020})
thisdict.update({"color": "red"})
thisdict.pop("model")
del thisdict["model"]
del thisdict
thisdict.clear()
for x, y in thisdict.items():
  print(x, y)
mydict = thisdict.copy()
mydict = dict(thisdict)

for x, obj in myfamily.items():
  print(x)

  for y in obj:
    print(y + ':', obj[y])
"""
clear()	Removes all the elements from the dictionary
copy()	Returns a copy of the dictionary
fromkeys()	Returns a dictionary with the specified keys and value
get()	Returns the value of the specified key
items()	Returns a list containing a tuple for each key value pair
keys()	Returns a list containing the dictionary's keys
pop()	Removes the element with the specified key
popitem()	Removes the last inserted key-value pair
setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
update()	Updates the dictionary with the specified key-value pairs
values()	Returns a list of all the values in the dictionary
"""