from gameElements.FactoryDisplay import FullDisplay
from gameElements.Tile import Tile
from gameElements.Board import PatternLines, Board
from tools.InputFixes import fixDisplayInput, fixMechanismInput, fixRandomGenerationInput
from tools.InputStyle import inputStyle, inputDisplay, inputColor, inputLine
from gameElements.Player import Player
##

## PICKING PHASE

# choose a display
def chooseDisplay(fullDisplay : FullDisplay,input_style : dict()):
    if fullDisplay.isEmpty():
        return 'FD1'
    display_name = inputDisplay(fullDisplay,input_style)
    try:
        display = fullDisplay.displays[display_name]
    except KeyError:
        print(f"The factory display '{display_name}' does not exist. Try again")
        return chooseDisplay(fullDisplay,input_style)
    
    if len(fullDisplay.displays[display_name].tiles) == 0:
        print("That factory display is empty. Please choose another one")
        return chooseDisplay(fullDisplay,input_style)
    print(f"You have picked the following display {display_name:} {Tile.p(fullDisplay.displays[display_name].tiles)}")
    
    return display_name

# choose a color
def chooseColor(fullDisplay : FullDisplay, display_name : str, input_style : dict()):
    display = fullDisplay.displays[display_name]
    avaiable_tiles = Tile.p(display.tiles)
    color = inputColor(fullDisplay,display_name,input_style)
    try:
        color = int(color)
        picked_tiles = fullDisplay.pickTiles(display_name,color)
    except TypeError:
        print(f"That's not a color (number). Try choosing from {set(avaiable_tiles)}")
        return chooseColor(fullDisplay, display_name,input_style)
    except ValueError:
        print(f"The color {color} is not available. Choose from {set(avaiable_tiles)}")
        return chooseColor(fullDisplay,display_name,input_style)
    print(f"You have picked the following color {color} tiles {Tile.p(picked_tiles)}")
    return picked_tiles

# choose a line
def chooseLine(patternLines : PatternLines, tiles: list, input_style : dict):

    if len(tiles) == 0:
        return
    tiles_to_place = Tile.p(tiles)
    line_index = inputLine(patternLines,tiles,input_style) 
    try:
        color = int(tiles[-1].color)
        line_index_int = int(line_index)
        patternLines.lines[line_index_int]
    except IndexError:
        print(f"The line {line_index_int} does not exist. Try choosing from {patternLines.validLinesToPlace(color)}: ")
        return chooseLine(patternLines,tiles,input_style)
    except ValueError:
        print(f"The line {line_index} does not exist. Try choosing from {patternLines.validLinesToPlace(color)}: ")
        return chooseLine(patternLines,tiles,input_style)
    print(f"You will place {tiles_to_place} in line {line_index}")

    return int(line_index)

# place tiles in the line
def action(board : Board, tiles, line_index : int):
    board.placeTilesInLine(tiles,line_index)

# enter the player name
def enterPlayerName(player : Player):
    name = input(f">> Please enter the name of player {player.name}: ")
    if name == "":
        name = player.name
    try:
        player.setName(name)
        print(f"Your chosen player name is: {name}")
    except TypeError:
        print("That is not a legal name. Try again.")
        return enterPlayerName(player)
    return name
    
# enter the playing style for player
def enterPlayStyle(player: Player):
    mechanism = input(f">> Choose the playing mechanism for Player {player.name}.\n"\
                       +"Type 'a' for automatic play, or type 'm' for manual play: ")
    
    mechanism = fixMechanismInput(mechanism)

    if mechanism not in ['automatic','manual']:
        print(mechanism,"You have to type 'a' for automatic play (i.e. bot), or 'm' for manual play (i.e. human). Try again.")
        return enterPlayStyle(player)

    input_style = inputStyle(mechanism,'better')

    if mechanism == 'automatic':
        adverb = 'automatically'
    elif mechanism == 'manual':
        adverb = 'manually'

    print(f"Player {player.name} will generate their input {adverb}.")
    
    return input_style