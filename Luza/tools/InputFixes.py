def fixDisplayInput(inp : str):
    if inp == 'c':
        return 'C'
    try:
        int(inp)
        return 'FD' + inp
    except ValueError:
        return inp

def fixMechanismInput(inp: str):
    if inp == 'm':
        return 'manual'
    elif inp == 'a':
        return 'automatic'
    elif inp == "":
        inp = 'automatic'
    return inp

def fixRandomGenerationInput(inp: str):
    if inp == 'k':
        return 'bad'
    elif inp == 'g':
        return 'good'
    elif inp == 'b':
        return 'better'
    elif inp == "":
        return 'better'
    return inp