import re

text = input()
pat = input()

x = re.findall(rf'[{pat}]',text)

print(len(x))
