# anagram is term where another word can derive from one word

def anagram(word1,word2):
    word1 = word1.lower()
    word2 = word2.lower()
    return sorted(word1) == sorted(word2)


print(anagram("shiv","vish"))