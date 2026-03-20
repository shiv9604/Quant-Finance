
'''  filter is used to filter out the values which are true according to applied function  '''

# syntax for filter = print(list(filter(function,list)))
def greater_5(num):
    if num>5:
        return True
    else:
        return False

# this function in lambda function...
greater_than_5 = lambda num: num>5 

l1 = [3, 4, 5, 6, 7, 8, 9, 98,78, 9, 8999]
filtered = list(filter(greater_5,l1))
filtered1 = list(filter(greater_than_5,l1))

print(filtered)
print(filtered1)

