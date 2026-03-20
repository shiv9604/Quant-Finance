''' 
In this programme we are going to count of the charecters of the string...
'''

dict = {}
print("Welcome to count of charecters programme...")
str = input("Enter the string without spaces : ")
# str = "shivisprogrammer"
def count_char(str):
    for i in str:
        countofchar = str.count(i)
        # print(f"{i} : {countofchar}")
        dict[i] = countofchar
    print(dict)

print(count_char(str))