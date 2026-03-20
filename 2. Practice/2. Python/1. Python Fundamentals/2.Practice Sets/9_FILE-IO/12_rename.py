# programme for rename the file names
import os
oldname = 'rename.txt'
newname = 'renamed.txt'
with open("rename.txt") as f:
    content = f.read()

with open("renamed.txt",'w') as f:
      f.write(content)

os.remove(oldname)

''' 
Logic used for renaming the file:
1.open the file and read the content
2.write that content into renamed.txt
3.delete the first file.
4.first file's data we put into renamed.txt after writing it will create new file named as renamed.txt
5.to pretend we renamed we have to remove the old file so it wil look like file renamed.

'''


    