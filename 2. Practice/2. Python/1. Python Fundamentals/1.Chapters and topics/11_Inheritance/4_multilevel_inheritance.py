
class person:
    country = "India"
    
    def takebreath(self):
        print("I am breathing...")

class employee(person):
    company = "Honda" 

    def takebreath(self):
        print("I am an employee and i am luckily  breathing...")

class programmer(employee):
    company = "Fiverr"

    def takebreath(self):
        print("I am an programmer and i got time for breathing...")

chirag = person()
print(chirag.country) # --> prints the conutry of person class
chirag.takebreath() # --> prints the takebrith of person class

sanj = employee() 
print(sanj.country) # --> prints the conutry of person class bcoz its a parent class
sanj.takebreath()  # --> prints the takebrith of employee class



shiv = programmer()
print(shiv.country) # it will print the country of employee which is from person class and programmer is child class of employee.
shiv.takebreath() # it will print the takebreath from its own class.
 