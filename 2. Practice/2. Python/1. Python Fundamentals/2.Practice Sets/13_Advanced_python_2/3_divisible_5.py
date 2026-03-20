
l1 = [7,14,21,28,35,42,49,56,63,70]

divisible = lambda num : num%5==0

print(list(filter(divisible,l1)))