# Programme for multiplication table in a new function
def table(n):
    for i in range(1,11):
        print(f"{n} x {i} = ",n * i)
    
    return " "

num = int(input("Enter the number : "))
print(table(num))
