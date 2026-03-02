import re

text = input()

pattern = r'ab{2,3}'

x = re.match(pattern, text)

if x:
    print("Yes")
else:
    print("No")
