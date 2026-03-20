# Default arguements
# programme for greeting someone 

def greet(name="Shiv"): # user is the parameter in the function
    return print("Good Morning, " + name)
# user = input("Enter your name : ")
# greet(user)

# greet() #--> we have to put the parameter value while calll
# in this we dont have to put the parameter value while call.
greet() # --> we can directly put our parameter value in function defination part.(name="Shivprasad")
greet("Sai") # --> it will overrides the value of name = "shiv" in the calling function.