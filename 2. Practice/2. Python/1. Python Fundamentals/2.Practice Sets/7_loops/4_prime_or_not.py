# Programme for check weather the num is prime or not.
num1 = int(input("Enter the number : "))
''' prime number is the number which is divisible by 1 and itself only'''
prime = False

for i in range(2,num1):
    if (num1%i == 0):
        prime = True
        break

if(prime):
    print("The number you entered is not prime number")
else:
    print("The number you entered is prime number")