from random import randint 

class board:
    def __init__(self):
        self.board = ["x","xx","xxx","xxxx","xxxxx"]
        self.matrix = ['abcde', 'bcdea', 'cdeab', 'deabc', 'eabcd']
        self.bottom = ""
        self.score = 0
    def print_board(self):
        print("dummy")


class game:
    def __init__(self, number_of_players : int):
        self.tiles_free = ["A"] * 20 + ["B"] * 20 + ["C"] * 20 + ["D"] * 20 + ["E"] * 20
        self.tiles_in_use = []
        self.num_of_rings = 2 * number_of_players + 1
        self.number_of_players = number_of_players
        self.boards = [[] for x in range(self.number_of_players)]
        self.player_to_play = 0

        # INTIALIZATION
        self.rings = [[] for x in range(self.num_of_rings)]
        self.midpot = ['X']
        self.rings_in_play = self.num_of_rings + 1
        self.check_if_consistent()
        self.deal_tiles()
        self.check_if_consistent()

    def deal_tiles(self):
        for i in range(len(self.rings)):
            for j in range(4):
                t = randint(0,len(self.tiles_free)-1)
                self.rings[i].append(self.tiles_free[t])
                self.tiles_in_use.append(self.tiles_free[t])
                del self.tiles_free[t]

    def check_if_consistent(self):
        if len(self.tiles_free) + len(self.tiles_in_use) != 100:
            print ("You have a bug in your code")
            return False
        return True

    def print_rings(self):
        print(" ")
        print("RINGS")
        print(" ")
        for i in range(self.num_of_rings):
            self.print_a_ring(i)
        print('0'+ " " + ''.join(self.midpot))

    def print_a_ring(self, ind : int):
        print(str(ind+1) + " " + ''.join(self.rings[ind]))

    def print_a_board(self,ind : int):
        print("Player" + str(ind+1) + " ", self.boards[ind])

    def print_boards(self):
        print(" ")
        print("BOARDS")
        print(" ")
        for i in range(self.number_of_players):
            self.print_a_board(i)

    def specify_command(self):
        self.last_command = input()
        print("You specified a command: " + self.last_command)

        # Making sure input is good

        if (len(self.last_command) != 2):
            print("Try again!")

        a = int(self.last_command[0])
        b = self.last_command[1]

        if (a not in range(self.num_of_rings+1)) or ((a != 0) and (b not in self.rings[a-1])) or ((a == 0) and (b not in self.midpot)):
            print("Try again!")
            self.specify_command()

        # Chosen ring is not the midpot
        if a != 0:
            for i in range(4):
                t = self.rings[a-1][i]
                if t == b:
                    self.boards[self.player_to_play].append(b)
                else:
                    self.midpot.append(t)
            self.rings[a-1] = []
            self.rings_in_play = self.rings_in_play - 1
                    
        # Chosen ring is the midpot
        if a == 0:
            A = [x for x in self.midpot]
            for i in range(len(A)):
                t = A[i]
                if (t == b) or (t == 'X'):
                    self.boards[self.player_to_play].append(t)
            self.midpot = [x for x in self.midpot if x != b]
            if 'X' in self.midpot:
                self.midpot.remove('X')

        # passes to the next player   
        self.player_to_play = (self.player_to_play + 1) % self.number_of_players

        self.print_rings()
        self.print_boards()


    def play(self):
        self.print_rings()
        self.print_boards()
        while (self.rings_in_play >= 1) and (self.midpot != []):
            self.specify_command()
        else:
            print('Round is over')
        

        


g = game(1)
g.play()