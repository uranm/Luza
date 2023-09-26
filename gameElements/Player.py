from gameElements.Board import Board
from tools.InputStyle import inputStyle

class Player:
    def __init__(self, name : str,input_style: dict() = inputStyle('manual','good')):
        self.name = name
        self.board = Board(self.name)
        self.input_style = input_style
        # self.first_player_next_round = False
    
    def setName(self, name):
        self.name = name
        self.board.name = name

    def setPlayStyle(self,input_style : dict()):
        self.input_style = input_style

    def __str__(self):
        name = self.name
        play_style = [self.input_style['mechanism']['line'],\
                      self.input_style['random_generation']['line']]
        board = self.board.__str__()

        playa_string = f"\033[4m PLAYER {name}, {play_style}\033[0m"

        return playa_string + "\n\n" + board