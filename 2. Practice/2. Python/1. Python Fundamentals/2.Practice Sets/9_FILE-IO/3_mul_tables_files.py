# Programme for create various different files in the tables folder

for i in range(2,20): # --> this for loop first start with 2
    with open(f"tables/multiplication_table_of_{i}","w") as f: # --> open and writes the file
        for j in range (1,11): # --> in this for loops starts for 2 by 1 to 11.
            f.write(f"{i} X {j} = {i*j}\n") # # --> in that file this for loop will print and write the table 0f 2
