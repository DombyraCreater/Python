import os
from pathlib import Path
import shutil

example = "Week6/example.jpg"

nested_dirs = Path("Week6/Data")
nested_dirs.mkdir(parents=True, exist_ok=True)
Path("Week6/Data/Backups").mkdir(parents=True, exist_ok=True)

file1 = nested_dirs / "image1.jpg"
file2 = nested_dirs / "notes.txt"
file3 = Path("Week6/Data/Backups/backup1.txt")

shutil.copyfile(example, "Week6/Data/image1.jpg")
file2.write_text("This is a text note", encoding="utf-8")
file3.write_text("This is a backup file", encoding="utf-8")

print("Contents of 'Week6/Data':")
for item in Path("Week6/Data").iterdir():
    print(item)

print("\nAll .txt files:")
for txt_file in Path("Week6/Data").rglob("*.txt"):
    print(txt_file)

shutil.copy(file2, Path("Week6/Data/Backups/notes_copy.txt"))
shutil.move(file1, Path("Week6/Data/Backups/image1_moved.jpg"))

print("\nAfter copying and moving:")
for item in Path("Week6/Data/Backups").iterdir():
    print(item)