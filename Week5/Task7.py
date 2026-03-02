import re

text = input()

def cam(match):
    return match.group(1).upper()

x = re.sub(r'_([a-z])', cam, text)

print(x)
