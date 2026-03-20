# use of readline function.

f = open("b.txt","rt") # --> 1) rb = read in binary mode.  2) rt = read in text mode(default)
# Reads the first line
d = f.readline() # --> Reads the line of file 
print(d)

# Reads the second line
d = f.readline() # --> Reads the line of file 
print(d)

# Reads the third line
d = f.readline() # --> Reads the line of file 
print(d)
