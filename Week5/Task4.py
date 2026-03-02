import re

text = input()

pattern = r'[A-Z][a-z]+'

x = re.findall(pattern, text)

if x:
    print("Yes")
    print(x)
else:
    print("No")
