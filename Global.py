x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
#x will change so the answer is "Python is fantastic" because x is global