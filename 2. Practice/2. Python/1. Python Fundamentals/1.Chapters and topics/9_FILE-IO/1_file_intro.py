# File open,read and to print its results.
f = open("b.txt","r") # --> opens the file # --> By default the mode is read mode r.
#d = f.read() # --> Reads the file 
e = f.read(5)
# print(d) # --> prints the contents of the file
print(e)
f.close()

'''  We can read the file only once. '''