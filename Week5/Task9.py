import re

text = input()

def ins(match):
    return " "+match.group(1)

x = re.sub(r'([A-Z])', ins, text)

x = x.lstrip()
print(x)
