# programme for understanding the constructor

class Employee:
        company = "Google"
        def getSalary(self,signature):
             print(f"Salary for the employee working in {self.company} is {self.salary}\n{signature}")
        
        def __init__(self,name,salary,subunit): # --> this funcrtion will run without calling. 
            print("The employee is created. ")
            self.name = name
            self.salary = salary
            self.subunit = subunit

        def getDetails(self):
            print(f"The name of the employee is {self.name}. ")
            print(f"The salary of the employee is {self.salary}. ")
            print(f"The subunit of the employee is {self.subunit}. ")
            
            
        @staticmethod
        def greet(signature):
            print("Good Morning, Sir")
            print(signature)  

shiv = Employee("shiv",1000,"facebook") # --> this will pass the arguements to getDetails bcoz we defined all there and we are calling all that in the getDetails().
# harry = Employee() # --> this will give the error bcoz there are 4 arguements we have to put inside the function call
shiv.getDetails() # --> it will give all the details of the employee.