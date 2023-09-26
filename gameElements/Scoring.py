## Scoring the building of a block
def computeBlockBuildScore(wall , line : int, color : int):
    wall_line = wall.wall[line-1]
    r = wall_line.index(color)
    c = line-1

    total_score = 1

    horizontal_score = 1
    vertical_score = 1

    horizontal_neighbors = False
    vertical_neighbors = False

    hr = 1
    while(r+hr <= 4 and wall_line[r+hr] % 10 == 0):
        horizontal_neighbors = True
        horizontal_score += 1
        hr += 1

    hl = 1
    while(r - hl >= 0 and wall_line[r-hl] % 10 == 0):
        horizontal_neighbors = True
        horizontal_score += 1
        hl += 1

    vd = 1
    while(c + vd <= 4 and wall.wall[c+vd][r] % 10 == 0):
        vertical_neighbors = True
        vertical_score += 1
        vd += 1

    vu = 1
    while(c - vu >= 0 and wall.wall[c-vu][r] % 10 == 0):
        vertical_neighbors = True
        vertical_score += 1
        vu += 1

    if not (horizontal_neighbors or vertical_neighbors):
        total_score = 1
    elif horizontal_neighbors and not vertical_neighbors:
        total_score = horizontal_score
    elif vertical_neighbors and not horizontal_neighbors:
        total_score = vertical_score
    else:
        total_score = vertical_score+horizontal_score

    return total_score

## Scoring the bonuses

# line bonuses
def lineBonus(line : list):

    for i in range(5):
        total = line[0]*line[1]*line[2]*line[3]*line[4]

    return 2 if total == 10*20*30*40*50  else 0

def lineBonuses(wall):
    score = 0
    for line in wall.wall:
        score += lineBonus(line)
    
    return score

# column bonuses
def columnBonus(wall, column_index :int):

    total = 1
    for line in wall.wall:
        total *= line[column_index]

    return 7 if total == 10*20*30*40*50 else 0

def columnBonuses(wall):
    score = 0
    for column_index in range(5):
        score += columnBonus(wall,column_index)
    return score

# color bonuses
def colorBonus(wall, color : int):
    count = 0
    for line in wall.wall:
        try:
            index = line.index(color)
        except ValueError:
            count += 1
    return 10 if count == 5 else 0

def colorBonuses(wall):

    score = 0
    for color in range(1,6):
        score += colorBonus(wall,color)
    
    return score