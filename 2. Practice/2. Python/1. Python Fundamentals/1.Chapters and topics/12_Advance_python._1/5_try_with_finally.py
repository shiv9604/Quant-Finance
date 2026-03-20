

try:
    a = int(input("Enter the number : "))
    b = 1/a
    print(b)
except Exception as e:
    print("Enter the valid integer value....")
    print(e)
    exit()
finally:
    print("If this is printing : Might be Some error occured!,Reconnecting...") # --> it will run at any cost...if error occured or doesnt!