#Students marks and sort it
m1 = int(input("Enter the makrs for student 1 : "))
m2 = int(input("Enter the makrs for student 2 : "))
m3 = int(input("Enter the makrs for student 3 : "))
m4 = int(input("Enter the makrs for student 4 : "))
m5 = int(input("Enter the makrs for student 5 : "))
m6 = int(input("Enter the makrs for student 6 : "))

marks = [m1,m2,m3,m4,m5,m6]
print(marks)
marks.sort()
print("The list of sorted marks of students is : ",marks)