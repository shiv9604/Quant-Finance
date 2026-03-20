# In this programme we are going to create the invoive by using python

#Company Details
company = "Iserices Ind,pvt Ltd."
adress = "Magarpatta city,Hadapsar"
pincode = "Pune 412308"

#Items and its pricing
item1,item2,item3,item4,item5 = "Iphone 11 Pro silicon cover","Oneplus OTG cable","Iphone OG lightning cable","Airpods 2","Iwatch series 6"
price_for_item1,price_for_item2,price_for_item3,price_for_item4,price_for_item5 = 499,899,2700,17000,24000
total = price_for_item1+price_for_item2+price_for_item3+price_for_item4+price_for_item5
greeting = "Thanks For shopping with us!"

#company  and adress block
print('*'*50)
print(f"\t{'-'*5}{company}{'-'*5}")
print(f"\t{adress}")
print(f"\t{pincode}")

#Items and pricing block
print('='*50)
print(f"{item1}\t{price_for_item1}")
print(f"{item2}\t\t{price_for_item2}")
print(f"{item3}\t{price_for_item3}")
print(f"{item4}\t\t\t{price_for_item4}")
print(f"{item5}\t\t\t{price_for_item5}")
print('='*50)

#Total block
print(f"\t\t\t\t{total}")
print('='*50)

#Greeting block
print(f'\t{greeting}')
print(f"{'*'*50}")
