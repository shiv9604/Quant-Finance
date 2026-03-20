# programme for introduction of inheritance

class employee: # Parent class
    company = "Google"

    def showdetails(self):
        print("This is an employee")

class programmer(employee): # single inharited child class
    language = "python"
    company = "Facebook"

    def showdetails(self):
        print("This is an programmer") # --> this will override the employee class function

# shiv = employee()
harry = programmer()
# print(shiv.company) 
# shiv.showdetails()

#Inherited class means derived class from employee
harry.showdetails() # --> this will give us the showdetails of employee class bcoz its parent class of programmer.
print(harry.company) 


        
    
    



