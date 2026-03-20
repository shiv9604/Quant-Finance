# programme to check file 1 is matches the content of file 2?

file1 = "log.txt"
file2 ="copy of log.txt"

with open(file1) as f:
    content1 =  f.read()

with open(file2) as g:
    content2 = g.read()

if content1 == content2:
    print("The files are identical and matches the content of each other.")
else:
    print("The files are not identical and the content doesn't matches to each other.")
