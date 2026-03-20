# Programme to find the natural numbers.
num1 = int(input("Enter the number : ")) 
i = 0
sum = 0
# sum = i + i
 # use while loop to iterate until zero
while(num1 > 0):
    sum += num1
    num1 -= 1
    print("The sum is", sum)