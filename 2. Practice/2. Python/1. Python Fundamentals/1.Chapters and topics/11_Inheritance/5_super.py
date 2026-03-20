''' 
super function is used to take value from parent class.
'''
class person:
    country = "India"
    
    def takebreath(self):
        print("I am breathing...")

class employee(person):
    company = "Honda" 
    
    def takebreath(self):
        super().takebreath()
        print("I am an employee and i am luckily  breathing...")

class programmer(employee):
    company = "Fiverr"
    
    def takebreath(self):
        super().takebreath()
        print("I am an programmer and i got time for breathing...")

chirag = person()
chirag.takebreath()

sanj = employee()
sanj.takebreath() # --> will print the function of parent class first ans after of own class.

shiv = programmer()
shiv.takebreath()
