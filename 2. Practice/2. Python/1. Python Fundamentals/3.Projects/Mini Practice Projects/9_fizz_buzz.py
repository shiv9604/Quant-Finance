# FizzBuzz Algorithm
# The FizzBuzz algorithm comes from a children’s game. This algorithm has been one of the favourite coding interview questions for a very long time. In this problem, you are given a range of integers and you need to produce output according to the rules mentioned below:

# If the integer (x) is divisible by 3, the output must be replaced by “Fizz”.
# If the integer (x) is divisible by 5, the output must be replaced by “Buzz”.
# If the integer (x) is divisible by 3 and 5, the output should be replaced by “FizzBuzz”

starting_value = int(input("Enter the start value of the range in which you want to apply fizz buzz algorithm : "))
stop_value = int(input("Enter the end value of the range in which you want to apply fizz buzz algorithm : "))

# range = (starting_value,stop_value)

def fizz_buzz(starting_value,stop_value):
    if starting_value < 0:
        print("Enter the valid start value greater than 0")
    for i in range(stop_value):
        if i%3==0 and i%6==0:
            print(f"{i} = FizzBuzz")
        elif i%3==0:
            print(f"{i} = Fizz")
        elif i%6==0:
            print(f"{i} = Buzz")
        else:
            print(i)

fizz_buzz(starting_value,stop_value)

