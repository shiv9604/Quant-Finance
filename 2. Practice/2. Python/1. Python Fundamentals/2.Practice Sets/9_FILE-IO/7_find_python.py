# Programme for finding the python in the log file

with open("log.txt") as f:
    read = f.read()

if "python" in read:
    print("Python keyword is there.")
else : 
    print("Python keyword is not there.")
