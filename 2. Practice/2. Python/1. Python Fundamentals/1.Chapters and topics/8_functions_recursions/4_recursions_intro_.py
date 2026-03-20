# introduction of recursions. # --> recursions are the functions called by itself("Khud ko call karne wala function")

# programme for factorial
#  n = 3

def factorial_func(n):
    product = 1
    for i in range(n):
        product = product * (i+1)
    return print(product)

factorial_func(5)

# factorial = 1 
#factorial = 1 x 2 x 3 x 4 x .... x n-1 x n
# formula creation = factorial * (n-1)
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n-1)

print(factorial_recursive(5))


