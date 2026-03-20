# programme for printing the line number of line containing the python.
read = True
i = 1
with open("log.txt") as f:
    while read:
        read = f.readline()

        if "python" in read:
            print(f"Python keyword is there at {i}")
        # else : 
        #     print("Python keyword is not there.")
        i +=1

'''
Logic for printing the line number is :
1.we are going to use the readline in while loop so it will read all the lines.
2.we are going to run the for if else condition for printing the line number.
3.Most Imp thing is {i} is going to give us the line number.
 ''' 