#Methods
a = {
    "fast": "Leopard is the fasteset.",
    "shiv": "A great programmer.",
    "marks" : [1,2,3], # --> we can add list inside the dict.
    "another_dict": {"chirag" : "bestfriend" } ,
    1 : 2
}

#Dictonary Keys
print(a.keys(),type(a.keys())) # --> Returns keys in different data type named as dict_keys. 

#Dictonary Values
print(a.values()) # --> Returns values in different data type named as dict_keys. 

#Dictonary items
print(a.items()) # --> Returns content of (keys,values) in different tuple data type. 

# Update (Add content Dictionary)
print(a)

a.update({"Love" : 3}) # --> adds "Love" : 3 in dict.
print(a)

#Update Dictionary
a.update({"marks": [33,33,33] }) # --> updates ( Overrides) the old values and updates the values of marks.
print(a)

# get method
print(a["shiv"]) #--> Gives the value of "shiv":
print(a.get("shiv")) #--> Also gives the value of "shiv":
# print(a["shiv3"]) #--> gives error if the key is not available in dict.
print(a.get("shiv3")) #--> Dont throws error instead of it will return none.


