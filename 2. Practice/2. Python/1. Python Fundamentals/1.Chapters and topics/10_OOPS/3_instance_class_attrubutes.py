# programme for instance attributes

class Employee:
    #Class attrubutes
    company = "Google" # class attributes
    salary = "3.5k"
    adress = "Banglore"

harry = Employee()
shiv = Employee()

# for printing the basic salary of harry and shiv which is mentioned in class.
print(harry.salary)
print(shiv.salary) # it will prints the class attributes values.

# Updating the salary(Instance attributes)
harry.salary = 3000 # instance attributes.
shiv.salary = 4000
print(f"The harry's salary after update is : ",harry.salary) #  it will prints the instance attributes.
print(f"The shiv's salary after update is : ",shiv.salary)

#IOnstance attributes which is not mentioned in the class object as well instance attributes
print(shiv.adress) # --> throws the error bcoz it's not defined.
 
