from gameElements.FactoryDisplay import FullDisplay, PickZone
from gameElements.Board import PatternLines
import random

## random factory displays
def randomDisplay(fullDisplay: FullDisplay, generation_style : str = 'good'):
    if generation_style == 'good':
        return goodRandomDisplay(fullDisplay)
    elif generation_style == 'bad':
        return badRandom()
    return "You have to specify a generation style for the displays."

def goodRandomDisplay(fullDisplay : FullDisplay):
    keys = [key for key in fullDisplay.displays.keys() if len(fullDisplay.displays[key].tiles) != 0]
    return random.choice(keys)

## random colors
def randomColor(display: PickZone, generation_style : str = 'good'):
    if generation_style == 'good':
        return goodRandomColor(display)
    elif generation_style == 'bad':
        return badRandom()
    return f"You have to specify a generation style for colors."

def goodRandomColor(display : PickZone):
    colors = list(set([tile.color for tile in display.tiles]))
    return random.choice(colors)

## random lines
def randomLine(patternLines : PatternLines, color : int,  generation_style : str = 'better'):
    if generation_style == 'better':
        return bestLine(patternLines,color)
    elif generation_style == 'good':
        return goodRandomLine(patternLines,color)
    elif generation_style == 'average':
        return averageRandomLine()
    elif generation_style == 'bad':
        return badRandom()
    return "You have to specify a generation style for lines."
    
    #
def goodRandomLine(patternLines: PatternLines, color : int):
    line_indices = patternLines.validLinesToPlace(color)
    if line_indices != []:
        print(f"You can place the tiles of color {color} in line {line_indices}")
        return random.choice(line_indices)
    else:
        print("You can only place these tiles on the floor")
        return -1
    
## best-chosen line
def bestLine(patternLines: PatternLines, color : int):
    line_indices = patternLines.validLinesToPlace(color)
    line_index = -1
    for index in line_indices:
        line = patternLines.lines[index-1]
        if line.color == color and not line.isComplete():

            line_index = index
            return line_index
    return goodRandomLine(patternLines,color)

#
def averageRandomLine():
    all_line_indices = [0,1,2,3,4,5]
    return random.choice(all_line_indices)

# generates a random character
def badRandom():
    return chr(random.randint(32,128))