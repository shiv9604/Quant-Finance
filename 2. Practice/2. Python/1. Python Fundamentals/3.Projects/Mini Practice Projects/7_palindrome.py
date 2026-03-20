# palindrome words are those words can be read as same as it will be reversed...

def palindrome(words):
    listofwords = words.split()
    palindrome_words = []
    for word in listofwords:
        if word[::1] == word[::-1]:
            palindrome_words.append(word)
    return palindrome_words

# words = input("Input the sentence in which you want to find the palindrome words : ")
words = "eye is not mom"
print(palindrome(words))