# programme for make a copy of any file
with open("log.txt") as f:
    content = f.read()

with open("copy of log.txt",'w') as f:
    f.write(content)

''' 
simple logic for copy.txt is 
1.read the content of the file you want to copy.
2.write that all content to copy.txt.
LOL...(((((LOl)))))
''' 