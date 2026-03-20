
def increment(num):
    try:
        return num + 1
    except:
        raise ValueError("This is not the proper value. ")

a = increment("shiv")
print(a)