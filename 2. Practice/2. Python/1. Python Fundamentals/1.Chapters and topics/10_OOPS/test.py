

class employee:
    company = "Google"
    
    def location(self,signature):
        print("location for shiv is pune.")
        print(signature)

    def getSalary(self):
        print(f"salary for shiv which is working in {self.company} is {self.salary}")

shiv = employee()
# shiv.salary = 1000
# print(shiv.salary)
# shiv.location("pune")
# shiv.getSalary() # prints the statement only.
shiv.salary = 2000 # if we want to update we have to mention self.salary in def function.
shiv.getSalary()

# programme for understanding of self function
class Employee:
        company = "Facebook"
        def getSalary(self): 
             
            print(f"Salary for the employee working in {self.company} is {self.salary}") # --> it will give the instance attributes value. This is only applied for function
            
shiv = Employee()
shiv.salary = 10000
shiv.company = "Twitter"
shiv.getSalary() 


class checkinit:
        def __init__ (self):
            print("employee is creaTED")

shiv = checkinit()