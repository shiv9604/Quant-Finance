# programme for Write the file 
f = open("b.txt","a")
data = f.write("This line is written by f.write function and in a = append mode.\n")
# print(data)
f.close()

# This will read the file.
f = open("b.txt","r")
d = f.read()
print(d)
f.close()
 
''' 
Difference between append('a') and write('w') mode.
1.In the write('w') mode existing data will erase and written data is only be there.
2.In the append('a') mode existing data will be there as well written data will add at the end of the file.
3.And in the both modes we can only use .write() to write someting in the file. 

''' 