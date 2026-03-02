import re

text = input()

pattern = r'[A-Z]'

x = re.split(pattern,text)

print(x)
