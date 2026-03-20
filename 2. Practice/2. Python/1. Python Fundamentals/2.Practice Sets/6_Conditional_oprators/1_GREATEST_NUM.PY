# programme to find greatest number.
num1 = int(input("Enter the number 1 : "))
num2 = int(input("Enter the number 2 : "))
num3 = int(input("Enter the number 3 : "))
num4 = int(input("Enter the number 4 : "))

''' In this we are using stratgy as:
    we are finding the winner in num 1 and num 2
    we are finding the winner in num 3 and num 4
    at last we are comparing the both winner and we are getting greatest number.

'''
if(num1>num2):
     g1 = num1
else:
    g1 = num2   

if(num3>num4):
     g2 = num3 
else:
     g2 = num4

if(g1>g2):
    print("The greatest number is :",g1)
else:
    print("The greatest number is :",g2)



