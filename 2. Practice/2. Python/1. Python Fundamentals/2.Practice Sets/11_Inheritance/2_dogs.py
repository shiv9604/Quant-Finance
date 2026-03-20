
class Animals:
    pass

class Pets(Animals):
    pass

class Dogs(Pets):
    
    def bark(self):
        print("Bhawwww Bhaww")

max = Dogs()
max.bark()