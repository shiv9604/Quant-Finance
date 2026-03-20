# To check wheather student is pass or not
m1 = int(input("Enter the marks of sub1 : "))
m2 = int(input("Enter the marks of sub2 : "))
m3 = int(input("Enter the marks of sub3 : "))

'''  
Logic we used for this program is :
1.fail conditions are more therfore we putted in if and elif bcoz 2 else are not possible.
2.in first condition each subject marks/percentage is less than 33 as per question then you are fail.
3.in second condition Total marks/percentage is less than 40 as per question then you are fail.
3.else you are passed
'''

if(m1<33 or m2<33 or m3<33):
    print("You are fail bcoz your percentage in one of the subjects less than 33%")
elif(m1+m2+m3)/3<40:
    print("You are fail bcoz your total percentage is less than 40% ")
else:
    print("Congratulations! ,You are passed")


