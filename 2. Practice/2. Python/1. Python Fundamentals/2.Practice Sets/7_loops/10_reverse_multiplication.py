## Programme for  reversed table inputed by user
num1 = int(input("Enter the number : ")) 

for i in range(10,1,-1):
    print(f"{num1} X {i} = {num1 * i}")

print("Your table is done!")