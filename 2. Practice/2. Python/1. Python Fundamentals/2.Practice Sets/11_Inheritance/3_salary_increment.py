
class employee:
    def __init__(self,salary,incrementperc):
        
        self.salary = salary
        print(f"The salary of Employee is : {self.salary}")
        
        self.incrementperc = incrementperc
        print(f"The increment percenatage of Employee is : {self.incrementperc}")

    @property
    def incrementrupees(self):
        return (self.salary * self.incrementperc) / 100
        
    @incrementrupees.setter
    def incrementrupees(self,costing):
        (self.salary * self.incrementperc) / 100
    
    @property
    def totalsalary(self):
        return self.salary + self.incrementrupees
        

    @totalsalary.setter
    def totalsalary(self):
        self.salary + self.incrementrupees
        
shiv = employee(5000,5)
print(shiv.incrementrupees)
print(shiv.totalsalary)
