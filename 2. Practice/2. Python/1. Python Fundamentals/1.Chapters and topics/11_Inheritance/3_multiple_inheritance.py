# Multiple inheritance means class is derived from multiple parents

class employee: # Parent class
    company = "Google"

    def showdetails(self):
        print("This is an employee")

class programmer(): # parent 2 class
    language = "python"
    company = "Facebook"

    
    
    def showdetails1(self):
        print("This is an programmer") # --> this will override the employee class function

class coder(employee,programmer): # child class derived from multiple parents
    codinglanguage = "C++"
    company = "Twitter"


shiv = coder()
print(shiv.company) # --> from class employee
print(shiv.language) # -->  from class programmer
# shiv.showdetails() 
print(shiv.codinglanguage) # -->  from class coder

''' 
Most Imp : if we want to print a detail which is mentioned in 2 parent classes then what will print?
--> (employee(1),programmer(2)) in checks what is first inside the class then it will print the first one (1).
'''
print(shiv.company) # this will print priority wise like (1:own class) , (2:class first mentioned in the class)



