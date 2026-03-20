'''
Lets assume we are going to find card in cards...
cards = alphabets  
progrmme for sequential search
'''

cards = ["A","B","C","D","E","F"]

def findcardseq(cardname):
    
    for card in cards:
        if card == cardname:
            print(f"{'-'*5} Card is matched with card {card} and YOUR CARD IS FOUND{'-'*5}")
        else:
            print(f" Card is not matched with card {card} and YOUR CARD IS NOT FOUND")

findcardseq("C")