a = int(input("Enter the number : "))
b = int(input("Enter the number : "))

try:
    print(a/b)
# except Exception as e:  
#      if b== 0: 
        #print("Infinite")
# except ZeroDivisionError:  
#      if b== 0: 
        #print("Infinite")
except:
    if b== 0: 
        print("Infinite")