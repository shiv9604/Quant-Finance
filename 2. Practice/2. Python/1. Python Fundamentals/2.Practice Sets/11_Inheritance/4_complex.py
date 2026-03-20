# formula for addition = (a+c) + (b+d)
# formula for multiplication = (a+bi)+(c+di) = (ac-bd) + (ad+bc)i

class complex:

    def __init__(self,r,i):
        self.real = r
        self.imaginory = i

    def __add__(self,c): # --> C is showing the another number. (5,10)
        return complex(self.real + c.real , self.imaginory + c.imaginory)
    
    def __str__(self):
        return f"{self.real} + {self.imaginory}i" # --> this is game changer. 
    
    
    def __mul__(self,c):
        mulreal = self.real*c.real - self.imaginory*c.imaginory # --> (ac-bd)
        mulimaginory = self.real*c.imaginory + self.imaginory*c.real # --> (ad+bc)i
    
        return complex(mulreal,mulimaginory)

a = complex(1,2)
b = complex(5,10)
print(a + b)
print(a * b)
