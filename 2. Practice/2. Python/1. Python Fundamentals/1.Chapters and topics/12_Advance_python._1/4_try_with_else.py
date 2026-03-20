
try:
    a = int(input("Enter the number : "))
    b = 1/a
except Exception as e:
    print("Enter the valid integer value....")
    print(e)
else:
    print(b)