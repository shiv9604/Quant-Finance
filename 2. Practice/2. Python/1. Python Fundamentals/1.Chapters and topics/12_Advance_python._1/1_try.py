
while(True):
    print("press q to quit")
    a = input("Enter the number: ")

    if a == 'q':
        break
    try: # --> try will run the keep runing the loop till it will recieve the error.
        print("Trying...")
        a = int(a)
        if a<6:
            print("Your entered number is greater than 6")
    except Exception as e: #--> this will print the error of which type and continue the loop instead of breaking the programme. 
        print(f"Your input resultated an error : {e}")

print("Thanks for playing")