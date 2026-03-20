#Dictionary finder
dict1 = {
        "kam" : "work",
        "sapne" : "dreams",
        "wastu" : "item"
}
user1 = input("Please enter the hindi word which you want to know in english : ")
# print("The english word for your entered word is :",dict1[user1])
print("The english word for your entered word is :",dict1.get(user1))
