# str __str__ methods

class number:
    
    def __init__(self,num):
        self.num = num

    def __str__(self):
        print(f"The number is : {self.num}") # it will avoid the other different result
    
    def __len__(self):
        return 1

a = number(5)
# print(a)
print(len(a))        
