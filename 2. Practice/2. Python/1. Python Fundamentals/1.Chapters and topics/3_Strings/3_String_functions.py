#String Functions

#len function
story = "once upon a time there was a great programmer Shiv"
print(len(story)) # --> Gives the lenth of string.

#.endswith function
print(story.endswith("Shiv")) #--> Checks and returns True and False.

#.Count functino
print(story.count("a")) # --> Counts the presence of a in string.

#.capitaliaze() function
print(story.capitalize()) # --> First charecter of string make capital.

#.find Method
print(story.find("shiv")) # --> Finds in the string and return the index of first occurance,and there will be not there it returns -1.

# .replace() function
print(story.replace("Shiv","Shivprasad")) # --> Replaces the content of string.