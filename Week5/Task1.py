import re

text = input()

pattern = r'ab*'

x = re.match(pattern, text)

if x:
    print("Yes")
else:
    print("No")
