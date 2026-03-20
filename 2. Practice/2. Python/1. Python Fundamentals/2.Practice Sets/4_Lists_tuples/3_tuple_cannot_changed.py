#Tuple cannot be changed
t1 = int(input("Enter the value for tuple : "))
t2 = int(input("Enter the value for tuple : "))
t3 = int(input("Enter the value for tuple : "))

tuple1 = (t1,t2,t3)
print(tuple1)

tuple1[1] = 3
print(tuple1)

