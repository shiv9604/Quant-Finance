

class Train:
    def __init__(self,name,seats,fare,AllSeats):
        self.name = name
        self.seats = seats
        self.fare = fare
       
    
    def getStatus(self):
        print(f"The name of train is {self.name} and the seats available are {self.seats}")
    
    def getFareInfo(self):
        print(f"The Fare for your train is : Rs.{self.fare}")
    
    def BookTicket (self):
        if self.seats>0:
            print(f"Your ticket is booked, and your seat number is {self.seats}")
            # print("Your ticket number is{self.seats} ")
            self.seats = self.seats-1
        else:
            print("The seats are not available please try for Tatkal...")
    def CancelTicket(self):
        print("Your ticket is cancelled sucessfully and your amount will be credited in some days.")
        self.seats = self.seats + 1

intercity = Train("Rajdhani express",2,2000)
# intercity.getStatus() # --> gives status
# intercity.BookTicket() #--> books first ticket
# intercity.getStatus() # give status with available seats bcoz one is booked and shows the remaining one.
# # intercity.getFareInfo()
# intercity.BookTicket()
intercity.getStatus()
intercity.BookTicket()
intercity.CancelTicket()
intercity.getStatus()
