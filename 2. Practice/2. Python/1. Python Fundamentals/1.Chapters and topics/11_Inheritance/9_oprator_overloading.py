''' 
oprator overloading khup soppa ahe.
Most Imp = fakt je internally call hotat methods tyala aplya hishobane modify karu shakto.
Use of :  class objects madhye aplyala jr mathmatical oprations perform karyche astin tr apan oprator overloaing karto.
''' 
class Number:

    def __init__(self,num):
        self.num = num
        
    def __add__(self,num2):
        print("lets add")
        # self.num = num2
        return self.num + num2.num # --> it will return 300 bcoz we modified add method .
    
    def __mul__(self,num3):
        print("lets multiply")
        # self.num = num2
        return self.num * num3.num


a = Number(5)
b =Number(5)
sum = a + b
mul = a * b
print(mul)
print(sum)