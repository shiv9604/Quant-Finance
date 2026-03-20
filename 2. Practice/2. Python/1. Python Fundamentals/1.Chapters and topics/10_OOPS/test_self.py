

class person:
    def greet(self):
        ''' 
        self:
        jr apan self takla soo kuthlya hi function apan call jr kela tr -->
        shiv.greet() or amol.greet() or anything.greet() hyatla shiv ,amol,anything he automatically self chya jagi janar.
        mg call ha Person.greet("shiv") evdha lihinyapeksha shiv.greet() jari lihila tari houn jata.
        self mule.....
        Most Imp --> kuthla pn funcrttion call jr dila tr self chya jagi  tyacha naw janar (naw = variable).
        '''
        print("Good Morning,")

shiv = person()
shiv.greet()