
''' 
Why to use _init__ 
jr aplyla class la arguements pass karyche astin tr aplyala __init__ use karyla lagte
else aplyala khelat basyla lagen
shiv.name = "shiv" asa
but jr __init__ use kela tr apan shiv = person("shiv") directly use karu shakto.

'''

class person:

    def __init__(self,name):
        self.name = name # if self is shiv then shiv.name will be name.

''' 
Calling __init__ mehod or attribute 
shiv = person(name) we have to pass the name while declaring the shiv is person.

'''
abhi = person("abhi")
print(abhi.name)
''' 
when we call abhi.name
1.abhi ha self honar soo abhi.name = name honar
2. name kay ahe apan pass kelela  abhi = person("abhi") "abhi"  he name honar. (self,name),abhi = person("abhi") hyatla name honar "abhi" honar.

'''