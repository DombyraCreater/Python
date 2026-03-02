import re

text = input()

pattern = r'a.*b'

x = re.match(pattern, text)

if x:
    print("Yes")
else:
    print("No")
