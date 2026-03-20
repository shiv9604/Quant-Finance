#progeramme for replace the list of words

words = ["car","bike","hayabusa"]

with open("donkey.txt") as f:
    text = f.read()



for word in words:
    text = word.replace(word,"333")
    
    with open("donkey.txt","w") as f:
        f.write(text)

