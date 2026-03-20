# programme for overriding the score in score.txt if score is greater.

def game():
    return 60

score = game()

with open("highscore.txt",'r') as f:
    highscore = int(f.read())

if highscore<score:
    with open("highscore.txt",'w') as f:
        f.write(str(score))
        