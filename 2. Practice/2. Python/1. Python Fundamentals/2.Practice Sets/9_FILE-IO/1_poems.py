# Programme for finding out the twinkle is in the poems.txt
with open("poems.txt") as poem:
    read =  poem.read()
    if 'twinkel' in poem:
        print("twinkel is there.")
    else:
        print("twinkel is not there.")
   