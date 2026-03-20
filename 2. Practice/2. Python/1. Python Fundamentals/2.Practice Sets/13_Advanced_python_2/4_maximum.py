from functools import reduce # --> this is most imp in the function of reduce.

l1 = [7,14,21,28,35,42,49,56,63,70]

value = reduce(max,l1)

print(value)
