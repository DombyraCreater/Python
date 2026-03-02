import re

text = input()

pattern = r'[a-z]+_[a-z]+'

x = re.findall(pattern, text)

if x:
    print("Yes")
else:
    print("No")
