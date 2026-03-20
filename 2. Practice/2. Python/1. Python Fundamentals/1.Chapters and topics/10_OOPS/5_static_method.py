# programme for understanding of static method.

class Employee:
        company = "Google"
        def getSalary(self,signature): # --> extra value shiv.greet(signature)
             print(f"Salary for the employee working in {self.company} is {self.salary}\n{signature}") # --> it will give the instance attributes value. This is only applied for function
            
        @staticmethod # --> it will run direcly shiv.greet() wiothout putting self
        def greet():
            print("Good Morning, Sir")
          #   print(signature) # --> signatue is the value extra value putted in the after sucessfull calling the function(shiv.greet("Thanks")) thanks is the signature.  

shiv = Employee()
shiv.salary = 10000 
# shiv.getSalary()  # --> Employee.getSalary(shiv)
shiv.greet()