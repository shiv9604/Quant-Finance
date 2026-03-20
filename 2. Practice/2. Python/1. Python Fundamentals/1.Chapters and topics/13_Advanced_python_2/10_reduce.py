
from functools import reduce

''' reduce applies rolling computation to the sequential pair of elements and returns a single value'''
sum = lambda a,b : a+b

l1 = [1,2,3,4]
final_val = reduce(sum,l1) # --> it will sum first 1+2=3 3+3 = 6 and finally 6+4 = 10 bcoz 10 is final value it returns 10.

print(final_val)

