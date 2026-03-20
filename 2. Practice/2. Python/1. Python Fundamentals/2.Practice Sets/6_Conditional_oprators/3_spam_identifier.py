#Checks its spam or not
text = input("Enter the comment: ")

''' 
We compared the user's text inut with the special strings if there it is it's a spam or else a not.

'''
if(text == "make a lot of money"):
    print("This is a spam comment.")
elif(text == "buy now"):
    print("This is a spam comment.")
elif(text == "suscribe this"):
    print("This is a spam comment.")
elif(text == "click this"):
    print("This is a spam comment.")
else:
    print("This is not a spam comment")


