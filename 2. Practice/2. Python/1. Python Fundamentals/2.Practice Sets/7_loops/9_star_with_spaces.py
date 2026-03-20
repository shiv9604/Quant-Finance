# printing the pattern of stars with spaces


num = int(input("Enter the number the much times you want to print * : "))
# num = 3

for i in range(num):
    print(" " * (num-i-1),end="")
    print("*" * (2*i+1),end="")
    print(" " * (num-i-1))

    # print(" " * 1,"*" * i)



