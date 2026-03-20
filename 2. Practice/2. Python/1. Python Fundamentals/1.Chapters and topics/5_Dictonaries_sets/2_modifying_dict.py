#Dict's are alterable and can be modified.
a = {
    "fast": "Leopard is the fasteset.",
    "shiv": "A great programmer.",
    "marks" : [1,2,3], # --> we can add list inside the dict.
    "another_dict": {"chirag" : "bestfriend" }
 

}
print(a)
print(a["marks"])

#Modification
a["marks"] = [3,3,3] 
print(a["marks"])

