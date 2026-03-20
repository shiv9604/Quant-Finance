# programme for remove the given word and strip the same time
# .strip() = removes unwanted spaces from the string

def rem_and_strp(string,word):
    remove = string.replace(word,"")
    strip = string.strip()
    return strip + remove  

str1 = "  shiv is a good programmer   "
print(rem_and_strp(str1,"a"))
