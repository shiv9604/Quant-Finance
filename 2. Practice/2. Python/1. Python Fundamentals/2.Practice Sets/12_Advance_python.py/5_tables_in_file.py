
user = int(input("Enter the number for which you want to print table : "))
l1 = [user*i for i in range(1,11)]
print(str(l1))

with open("Tables.txt",'w') as f:
    f.write(str(l1))
    f.write('\n')
