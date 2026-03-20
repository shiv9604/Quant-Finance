#Lists
a = [1,2,23,4,56,78]
print(a) 
''' 
Lists are Changable and alterable ex; a[0] = 5
List includes items of different or multiple data types
'''

#list indexing
print(a[1])

#List modification and updation
a[2] = 3 # --> a[Index] changes the value of 2 index = 23.
print(a) 

#List slicing
friends = ["shiv","Chirag","raju","sanjana","shruti",33]
friends[2] = "Swapnali" 
print(friends[:4])