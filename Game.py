from gameElements.FactoryDisplay import FullDisplay
from gameElements.Bag import Bag
from gameElements.Player import Player
from interactiveMessages.Commands import chooseDisplay, chooseColor, chooseLine, action
from interactiveMessages.Commands import enterPlayerName, enterPlayStyle
import time

# this is the turn a player plays on the display
class Turn:
    def __init__(self, display : FullDisplay, player : Player):
        self.display = display
        self.player = player
        self.input_style = self.player.input_style
    
    def play(self):
        print(self.beginTurnMessage())
        board = self.player.board
        input_style = self.input_style
        display_name = chooseDisplay(self.display,input_style)
        tiles = chooseColor(self.display,display_name,input_style)
        line = chooseLine(board.patternLines,tiles,input_style)
        action(board,tiles,line)
        print(board)
        print(self.endTurnMessage())
        

    
    def beginTurnMessage(self):
        str0 = "____________________________"
        str1 = f"It is player {self.player.name}'s turn."
        return str0 + "\n" + str1 + "\n" + str0 + "\n" +\
              "\n" + self.display.__str__() + "\n" + self.player.board.__str__()
    
    def endTurnMessage(self):
        str1 = f"Player {self.player.name}'s turn is done."
        str0 = "____________________________"
        return str0 + "\n" + str1 + "\n" + str0 + "\n"

# this is the round all the players play in
class Round:
    def __init__(self, display: FullDisplay, players : list, first_player : int,  round_number:int=0):
        self.round_number = round_number
        self.display = display
        self.players = players
        self.currentPlayerIndex = first_player
        self.next_round_first_player = None

    # goes to next player who will play the next turn
    def nextPlayer(self):
        nr_players = len(self.players)
        self.currentPlayerIndex = (self.currentPlayerIndex + 1) % nr_players       
        return self.currentPlayerIndex
    
    # player plays their turn
    def playTurn(self, player):
        turn = Turn(self.display, player)
        return turn.play()

    # play a round
    def play(self):
        print(self.beginRoundMessage()+ "\n")
        
        while not self.display.isEmpty():
            player = self.players[self.currentPlayerIndex]
            input(f">> Press 'Enter' to start {player.name}'s turn.")
            print("\n")
            self.playTurn(player)
            self.currentPlayerIndex = self.nextPlayer()
        print(self.endRoundMessage()+"\n")
        
    
    # determines first player for next round
    def determineNextFirstPlayer(self):
        for i in range(len(self.players)):
            player = self.players[i]
            check = player.board.checkIf0OnFloor()
            if check:
                return i
        return
    
    # round end activities for one player
    def endRoundForPlayer(self, player : Player):
        board = player.board
        board.buildAllBlocks()
        board.computeFloorScore()
        board.clearFloor()
        
    # round end activities for all players
    def endRoundForAll(self):
        for player in self.players:
            self.endRoundForPlayer(player)

    def recycleExtraTiles(self):
        extraTiles = []
        for player in self.players:
            extraTiles += player.board.extraTiles
            player.board.extraTiles = []
        return extraTiles
    
    def beginRoundMessage(self):
        str0 = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        str1 = f"Round {self.round_number}"
        str2 = "Players: "
        for player in self.players:
            str2 += f"{player.name},"
        return str0 + "\n" + str1 + "\n" + str2[:-1] + "." +"\n" + str0
    
    def endRoundMessage(self):
        str0 = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        str1 = f"Round {self.round_number} is finished."
        return str0 + "\n" + str1 + "\n" + str0

# this is the game class, encodes all the game elements and mechanisms
class Game:
    def __init__(self, nr_players : int):
        self.bag = Bag(100)
        nr_displays = 2*nr_players + 1
        self.fullDisplay = FullDisplay(nr_displays)
        self.players = [Player(f"{i+1}") for i in range(nr_players)]
        self.extraTiles = []
        self.roundNumber = 1

    def enterPlayerDetails(self):
        for player in self.players:
            name = enterPlayerName(player)
            player.setName(name)
            print("\n")
            input_style = enterPlayStyle(player)
            player.setPlayStyle(input_style)
            print("\n")
#  
    def refillBag(self):
        if self.extraTiles != []:
            self.bag.refillBag(self.extraTiles)
        self.extraTiles = []

# def
    def collectExtraTiles(self):
        for player in self.players:
            extraTiles = player.board.extraTiles
            self.extraTiles += extraTiles
            player.board.extraTiles = []

    def updateGameOver(self):
        gameOverList = []
        for player in self.players:
            gameOver_player = player.board.wall.gameOver
            gameOverList.append(gameOver_player)
        return any(gameOverList)
    
    def computeBonuses(self):
        for player in self.players:
            player.board.computeBonuses()

    def getFinalRanking(self):
        final_ranking = sorted(self.players,key=lambda player : -player.board.score)
        return final_ranking

    def endOfGameMessage(self):
        str0 = "####################### GAME OVER #######################"
        str1 = "#########################################################"
        final_ranking = self.getFinalRanking()
        ranking = "The final ranking of the players is: "
        ranks = ""
        rank = 1

        input(f">> The game is over. Press 'Enter' to compute the bonus scores and get the final ranking.")

        for player in final_ranking:
            ranks += f"{rank}. {player.name}, {player.board.score} points   \n"
        print("\n"+str1 +"\n" + str0 + "\n" + str1 + "\n\n" + ranking + "\n" +ranks)

    def play(self):
        bag = self.bag
        d = self.fullDisplay
        bag.fillFullDisplay(d)
        players = self.players
        roundNumber = self.roundNumber
        first_player_round = 0
        gameOver = False

        while not gameOver:
            input(f">> Press 'Enter' to start round {roundNumber}.")
            print("\n")
            round = Round(d,players,first_player_round, roundNumber)
            round.play()
            first_player_round = round.determineNextFirstPlayer()
            input(">> Press 'Enter' to compute the scores of this round.")
            print("\n")
            round.endRoundForAll()
            self.extraTiles += round.recycleExtraTiles()
            bag.fillFullDisplay(d)
            roundNumber += 1
            gameOver = self.updateGameOver()
            
            for player in self.players:
                print(player.board)

            if bag.isEmpty():
                self.refillBag()

        # print("\n")
        # input(f">> The game is over. Press 'Enter' to compute the bonus scores and get the final ranking.")
        self.computeBonuses()
        
        # print(self.endOfGameMessage())
        