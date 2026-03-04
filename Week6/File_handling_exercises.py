import shutil

file = "Week6/sample.txt"

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

with open(file, 'a', encoding='utf-8') as f:
    f.write(" Hello Friends\n")

with open(file, 'r', encoding='utf-8') as f:
    print("After append:")
    newcontent = f.read()
    print(newcontent)

shutil.copyfile(file,"Week6/Copy.txt")
print("copied")

shutil.os.remove(file)