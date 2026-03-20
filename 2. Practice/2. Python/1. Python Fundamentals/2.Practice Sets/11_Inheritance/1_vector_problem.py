
class c2Dvec:
    vector = "2D"
    print("This is a c2dvec 2D vector class...")

class c3Dvec(c2Dvec):
        vectorof3d = "3D"
        print("This is a c3dvec 3D vector class...")

a = c2Dvec()
b = c3Dvec()
print(b.vector) # --> this is printing the vector of 2D which is parent's Class.
print(b.vectorof3d)

