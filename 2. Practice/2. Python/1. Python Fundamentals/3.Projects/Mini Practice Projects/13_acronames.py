#An acronym is a short form of a word created by long words or phrases such as NLP for natural language processing
# In this programme we are going to write the programme for creating the acronames

word = input("Enter the word which you want to acronise : " )

def acronise(word):
    text = word.split()
    for i in text:
        print(i[0].upper(),end='')

acronise(word)