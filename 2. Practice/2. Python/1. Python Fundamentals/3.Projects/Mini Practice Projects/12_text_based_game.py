# we are going to make text based adventure game in which we are putting the situation and you have to choose the option..
# to the reach the next level you have to go with the right options
import sys
name = input("Enter your name : ")
print(f"Hello {name}! Welcome to the adventure game created by shiv")
print("Are you ready to start the game ? \n If Yes press 1,or else 2")

ready = int(input("Enter here wheather you are ready or not ? :  "))
if ready == 1:
    print("We are creating the task for you wait a min plz..")
elif ready ==2:
    print("Start the game again when you will be ready..")
    exit()
else:
    print("Enter the valid input as per instructions")

situation = print("You are stucked at the fire place, What you will do to effective result on fire?")
print("Press 1 to spread the sand on the fire")
print("Press 2 to spread the water on the fire")
solution = int(input("Enter Your response which will be more effective on the fire : "))

while(True):
    situation = print("You are stucked at the fire place, What you will do to effective result on fire?")
    print("Press 1 to spread the sand on the fire")
    print("Press 2 to spread the water on the fire")
    # solution = int(input("Enter Your response which will be more effective on the fire : "))
    if solution ==1:
        print("Sand is more effective than the water as the fire extinguisher")
        print(f"\n{'#' * 5} Congratulations! You won the game {'#' * 5}\n")
        exit()
    elif solution ==2:
        print("Sand is more effective than the water as the fire extinguisher")
        print(f"\n{'*' * 5} Oops! You lose the game {'*' * 5}\n")
        exit()
    else:
        print(f"\n{'-' * 5}Enter the valid input as per instructions{'-' * 5}\n")
        
    solution = int(input("Enter Your response which will be more effective on the fire : "))






