# programme for introduction of inheritance

class employee: # Parent class
    company = "Google"

    def showdetails(self):
        print("This is an employee")

class programmer(employee): # child class
    language = "python"
    company = "Facebook"

    def showdetails(self):
        print("This is an programmer") # --> this will override the employee class function
''' 
In inheritance nothing is special
1) it means child class will give the details of parent class until it's mentioned in child class.
2) if we put details in child class it will overrides the details of parent class.
'''

# shiv = employee()
harry = programmer()
# print(shiv.company) 
# shiv.showdetails()

#Inherited class means derived class from employee
harry.showdetails() # --> this will give us the showdetails of employee class bcoz its parent class of programmer.
print(harry.company) 


        
    
    



