
try:
    a = int(input("Plese enter the number : "))
    b = 1/a
    print(b)
except ValueError as e:
    print("Please Enter the valid integer value")
    # print(e) 
except ZeroDivisionError as e:
    print("Make sure you are not dividing by 0")
    # print(e) # --> this willl print the error which is occuring.
except Exception as e:
    print("Something went wrong!,Please try again with 0 mistakes...")
    # print(e) 

print("Thanks for using this code.")