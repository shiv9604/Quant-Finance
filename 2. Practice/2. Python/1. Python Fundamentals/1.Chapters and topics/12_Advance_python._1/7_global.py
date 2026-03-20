
a = 5 # --> Global value
def func1():
    global a # --> this will use global variable.
    a = 3 # --> this will update the value of global value.
    print(f"The local variale is : {a}")

func1()
print(f"The global variable is : {a}")