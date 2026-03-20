# introduction of function.
''' 1.percentage = sum of marks/400(out of marks) * 100
    gives the percentage

    2. average = sum of marks/no of marks    
''' 
def avg(marks): # def called as defination part.
   #function body
    return sum(marks)/len(marks)

marks1 = [10,20,30,40,50]
print(avg(marks1)) # calling part