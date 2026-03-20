# We have to install tabulate module in our psystem interpretator
# we have to note that we can use tabulate module with :
# Lists
# Dictionary
# NumPy Array
# Pandas DataFrame
# structure(data,headers='firstrow',tablefmt='format which we want')

from tabulate import tabulate

data = [["Name","Age","DOB"],["Shiv",18,28/8/2002],["Madhav",49,15/7/1971]]
print(tabulate(data,headers='firstrow',tablefmt='orgtbl'))