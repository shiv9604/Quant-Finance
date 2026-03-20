# Set Add
a = set()
print(a)

a.add(3)
print(a)

# Data types which can be add in set
a.add((2,3,4)) # --> We can addd tuple to set
print(a)


#If your data type is not hashable then you cannot add it to sets. ( non Hashable : a data type which can be changed or alterable(immutable)) 
a.add({2:4}) # --> We cannot add DICTIONARY to set
a.add([2,3,4]) # --> We cannot add list to set

