# programme for introduction of class and building the first class.
class Employee:
    company = "Google"
    salary = 1000

harry = Employee()  # --> harry is employee 
shiv = Employee()  # --> shiv is employee
print(harry.company) # --> it will print the harrys company which is mentioned in class.
print(shiv.company) # --> it will print the shiv's company which is mentioned in class.

Employee.company = "Facebook"
print(harry.company) # --> it will print the harrys changed company which is mentioned in class.
print(shiv.company) # --> it will print the shiv's changed company which is mentioned in class.

shiv.company = "Microsoft" # --> it will only change the company of only shiv
harry.company = "Twitter" # --> it will only change the company of only harry
print(shiv.company)
print(harry.company)

shiv.salary = 300 # --> it will override the value of salary 1000 to 300
harry.salary = 400 # --> it will override the value of salary 1000 to 400
print(shiv.salary)
print(harry.salary)

