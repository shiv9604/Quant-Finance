
''' 
if __name__ == '__main__'
used to if we dont want to print some part of code in another imported file then we use it.
in another imported file the above that code can be used.
'''
def greet(name):
    return print(f"Good Morning,{name}")

# print(__name__)
if __name__ == '__main__':
# --> under this code part will not run in imported file.
    a = input("enter your name : ")
    greet(a)
