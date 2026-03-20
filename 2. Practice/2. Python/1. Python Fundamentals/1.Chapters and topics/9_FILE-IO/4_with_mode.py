# with mode for opening and closing and opening the files in any mode.
with open("b.txt") as e: # --> it skips the closing of file. e is a varibale which can be named as anything.
    f = e.read()
    print(f)