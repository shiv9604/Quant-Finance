# break statement in for loop or while loop

for i in range(9):
    print(i)
    if i == 5: #--> when this condition becomes true it will stop the loop.
        break; 
else:
    print("This is inside the else statement.")  

''' 
else will not print bcoz it returns only when loops sucessfull termination(Naturally ends the loop then else only returns).
in this break statement this is not exited naturallly it willl not get executed.
'''        
