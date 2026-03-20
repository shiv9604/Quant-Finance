#Dictonaries
a = {
    "fast": "Leopard is the fasteset.",
    "shiv": "A great programmer.",
    "marks" : [1,2,3], # --> we can add list inside the dict.
    "another_dict": {"chirag" : "bestfriend" }
 

}
print(a)

#Indexing
# print(a["shiv"]) # --> prints the value of the spcific key["Shiv"]]we inserted.
# print(a["fast"]) # --> prints the value of the spcific key["fast"] we inserted.
# print(a["marks"]) # --> prints the value of the spcific key["marks"] we inserted.

print(a["another_dict"]) # --> prints the value of the spcific key["another_dict"] we inserted.
print(a["another_dict"]["chirag"]) # --> prints the value of the spcific key["chirag"] inside the nested dict another_dict.
