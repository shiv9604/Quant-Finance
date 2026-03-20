# programme for understanding of self function
class Employee:
        company = "Google"
        def getSalary(self): 
            '''
            self: 
             1.self is a parameter which passed automatically
             2.used to shorten the call we can directly call shiv.getSalary() instead of Employee.getSalary(shiv).
             3.if self is not given it will throws the error.

             use:
             1.We can use class attributes as well as instance attributes as well as class attributes.
             2.if we use self.salary (shiv.salary = 100000) so it will print the intance salary for the spcific employee.
            ''' 
            print(f"Salary for the employee working in {self.company} is {self.salary}") # --> it will give the instance attributes value. This is only applied for function
            # If we are not using the function then we can add directly instance attributes and print them.
            # self.company will give us the value of company for the employee shiv.

shiv = Employee()
shiv.salary = 10000 # --> we have to write self.salary inide the function to print the updated salary.
shiv.getSalary() # --> this will not print the updated salary bcoz we didnt used self.salary in the class attributes.

    