score = 0

def inc_score():
    global score
    score += 1

def get_score():
    return str(score)


lives = 3

def lose_life():
    global lives
    lives -= 1

def get_lives():
    return str(lives)
