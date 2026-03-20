# programme to find the factorial of a given number.
# 6 is 1*2*3*4*5*6 = 720
num = int(input("Enter the num: ")) 
factorial = 1

for i in range(1,num+1):
    factorial = factorial * i
print(f"The factorial of this {num} is {factorial}.") 

''' 
Remember!!!!!!!!!!!!!!
print the loop outside the 4 spaces else it will not give proper result

 '''
    
