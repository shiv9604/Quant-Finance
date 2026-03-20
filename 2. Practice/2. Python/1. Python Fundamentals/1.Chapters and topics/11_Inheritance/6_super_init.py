
''' 
super __init__ is used to take value of __init__ from parent class aS own and parent class as well.
'''
class person:
    country = "India"

    def __init__(self):
        print("Initializing person....")
    
    def takebreath(self):
        print("I am breathing...")

class employee(person):
    company = "Honda" 
    
    def __init__(self):
        super().__init__()
        print("Initializing employee....")

    def takebreath(self):
        super().takebreath()
        print("I am an employee and i am luckily  breathing...")

class programmer(employee):
    company = "Fiverr"
    
    def __init__(self):
        super().__init__()
        print("Initializing programmer....")
    
    def takebreath(self):
        super().takebreath()
        print("I am an programmer and i got time for breathing...")

chirag = person()


sanj = employee()


shiv = programmer()

