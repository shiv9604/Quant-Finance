
''' map function is used to commonly apply the function to all the items '''

l1= [2,3,4]
square = lambda num: num*num
# if we want to apply the square to all of this items then ...

#Method 1 with for loop
l2 = []
for i in l1:
    l2.append(square(i))
print(l2)

# Method 2 by map function.
mapped = map(square,l1)
print(list(mapped))