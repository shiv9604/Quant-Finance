# write a recursive function for sum of first n natural numbers
# sum of first n natural numbers = 1 + 2 + 3 + 4 + 5...n
# formula =

# def factorial_recursive(n):
#     if n == 0 or n == 1:
#         return 1
#     return n * factorial_recursive(n-1)

# print(factorial_recursive(5))

def sumN(n):
    if n <= 0:
        return 0
    elif n ==1:
        return 1
    else:
        return n + sumN(n-1)

print(sumN(-1))