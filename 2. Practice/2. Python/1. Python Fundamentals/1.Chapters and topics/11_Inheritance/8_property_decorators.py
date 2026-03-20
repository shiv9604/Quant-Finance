
class employee:
    company = "Bhatat Gas"
    salary = 5000
    bonus = 500
    # totalsalary = 5000 in future we have to change the both values.
# to avoid that we are creating the function.

    @property # it wil convert as a property of class it is also called as getter.
    def totalsalary(self):
        return self.salary + self.bonus

    @totalsalary.setter # it will call the automatically this function.
    def totalsalary(self,val):
        self.salarybonus = val - self.salary # it wil give the value of salary bonus bonus = total salary - salary
        

shiv = employee()
# print(shiv.totalsalary)
print(shiv.salary)
# AFTER CHANGING THE BONUS VALUE
# shiv.bonus = 100
# print(shiv.totalsalary)

#IF WE CHANGE TOTAL SALARY THEN HOW IT WILL  CONVERT INTO SALARY AND BONUS
shiv.totalsalary = 6100
print(shiv.salarybonus) 
print(shiv.salary)