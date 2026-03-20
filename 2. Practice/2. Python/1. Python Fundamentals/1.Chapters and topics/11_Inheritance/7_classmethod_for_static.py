''' If we want to change value inside the class then we use @classmethod '''

class employee:
    company = "Google"
    salary = 500
    location = "pune"


    # def changesalary(self,sal):
    #     self.salary = sal # --> it will only add the instance attribute not changes the class method
    
    @classmethod
    def changesalaryClass(cls,sal):
        cls.salary = sal # --> it will only add the instance attribute not changes the class method

    

shiv = employee()
# # before addign instance attribute
# print(f"The salary before adding instance attribute is :  {shiv.salary}")

# # After adding the instance attribute

# shiv.changesalary(600)
# print(f"The salary after adding instance attribute is :  {shiv.salary}")

# BUT !!!!! After changing the class attribute
print(f"The orignal salary of shiv before changing class attribute is : {shiv.salary}")

# changing the class attribute by using @classmethod
shiv.changesalaryClass(1000)
print(f"The salary after adding instance attribute is :  {shiv.salary}")

# after changed class attribute 
print(f"The salary of shiv after changing class attribute is : {shiv.salary}")


