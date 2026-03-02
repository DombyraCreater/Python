import re

text = input()

pattern = r'[\s,.]'

x = re.sub(pattern, ":" ,text)

print(x)
