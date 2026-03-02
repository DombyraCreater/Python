import re

text = input()

def sna(match):
    return "_"+match.group(1).lower()

x = re.sub(r'([A-Z])', sna, text)

print(x)
