from gameElements.FactoryDisplay import FullDisplay
from gameElements.Tile import Tile
from gameElements.Board import PatternLines
from tools.RandomInputGenerator import randomDisplay, randomColor, randomLine
from tools.InputFixes import fixDisplayInput

# input_style = dict()
# input_style['mechanism'] = dict()
# input_style['random_generation'] = dict()

# input_generation_style = 'good'
# input_mechanism = 'manual'

# input_style['mechanism']['display'] = input_mechanism
# input_style['mechanism']['color'] = input_mechanism
# input_style['mechanism']['line'] = input_mechanism

# input_style['random_generation']['display'] = input_generation_style
# input_style['random_generation']['color'] = input_generation_style
# input_style['random_generation']['line'] = input_generation_style

#
def inputStyle(mechanism: str, random_generation: str):
    input_style = dict()

    if random_generation == 'better':
        input_style = inputStyle(mechanism, 'good')
        input_style['random_generation']['line'] = 'better'
        return input_style
    
    input_style['mechanism'] = dict()
    input_style['random_generation'] = dict()

    input_style['mechanism']['display'] = mechanism
    input_style['mechanism']['color'] = mechanism
    input_style['mechanism']['line'] = mechanism

    input_style['random_generation']['display'] = random_generation
    input_style['random_generation']['color'] = random_generation
    input_style['random_generation']['line'] = random_generation

    return input_style

def inputDisplay(fullDisplay: FullDisplay , input_style : dict):

    generation_style = input_style['random_generation']['display']

    if input_style['mechanism']['display'] == 'automatic':
        display_name = randomDisplay(fullDisplay,generation_style)
        return display_name
    elif input_style['mechanism']['display'] == 'manual':
        display_name = input(">> Choose a factory display: ")
        display_name = fixDisplayInput(display_name)
        if display_name == "":
            display_name = randomDisplay(fullDisplay, generation_style)
        return display_name
    return

def inputColor(fullDisplay : FullDisplay, display_name : str, input_style : dict):
    generation_style = input_style['random_generation']['color']
    display = fullDisplay.displays[display_name]

    if input_style['mechanism']['color'] == 'automatic':
        color = randomColor(display,generation_style)
        return color
    elif input_style['mechanism']['color'] == 'manual':
        color = input(">> Choose a color: ")
        if color == "":
            color = randomColor(display, generation_style)
        return color
    return

def inputLine(patternLines : PatternLines, tiles : list, input_style : dict):
    generation_style = input_style['random_generation']['line']
    tiles_to_place = Tile.p(tiles)

    if input_style['mechanism']['line'] == 'automatic':
        line_index = randomLine(patternLines,tiles[-1].color,generation_style)
        return line_index
    elif input_style['mechanism']['line'] == 'manual':
        line_index = input(f">> Choose a line to place the tiles {tiles_to_place}: ")
        if line_index == "":
            line_index = randomLine(patternLines,tiles[-1].color,generation_style)
        return line_index
    return
