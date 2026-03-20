# programme for writing the ### instead of donkey multiple times
# with open("donkey.txt","w") as f:
#     f.write("donkey donkey donkey")
#     f.write("donkey donkey donkey")
#     f.write("donkey donkey donkey")
#     f.write("donkey donkey donkey")
with open("donkey.txt") as f:
    text = f.read()

with open("donkey.txt","w") as f:
    replace = text.replace("donkey","#####")
    f.write(replace)