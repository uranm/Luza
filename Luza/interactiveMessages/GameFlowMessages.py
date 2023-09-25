from Game import Game

def beginningOfGameMessage():
        str0 = "#########################################################"
        str1 = "####################### LUZA ############################"
        print("\n"+str0 + "\n" + str1 + "\n" + str0)
        print("\n")

        welcome = "Welcome to LUZA: an implementation of the board game Azul."
        explanation = "For the rules of the game, see https://www.ultraboardgames.com/azul/game-rules.php. "\
            +"LUZA works exactly like Azul with the following visual differences: \n" \
                "1. Instead of colored tiles, we use tiles numbered with 1, 2, 3, 4, 5.\n"\
                    +"2. The penalty tile, marked 1 in Azul, is marked 0 in LUZA\n" \
                        +"3. The wall of the game signifies a built block by multiplying that number by 10."
        print(welcome + "\n\n" + explanation +"\n")
        expl = input(">> Press 'y' if you want to see how you can interact with the game. Press 'Enter' to directly start a game: ")
        if expl == 'y':
            gameflow_explanation = "You will first be asked to provide the number of players, between 1 and 4. Next, you will be asked "\
                +"to specify the name of each player, and whether their inputs will be manual (i.e. human player) or automatically generated "\
                    +"(i.e. bot player). Even though the bot players play legal moves, they are generally horrible at the game :)."
            print("\n" + gameflow_explanation + "\n")
            input(">> Press 'Enter' to continue.")
            gameflow_explanation2 = "After the players specifics have been defined, the game will start with the first player. On their" \
                +" turn, a player will have to provide three commands: 1. Select a factory display by pressing one of the keys: "\
                    +"1,2,3,4,5,c. 2. Select all the tiles of a given color from the factory display, by pressing one of the keys: "\
                        +"1,2,3,4,5. 3. Select a line of your board where you want the tiles to be placed, by pressing one of the keys: "\
                            +"1,2,3,4,5,0. The last key 0 means that the tiles will be placed on the bottom floor line, which contribute "\
                                +"negative points (so try to not do that :))"
            print("\n" + gameflow_explanation2 + "\n")
            input(">> Press 'Enter' to continue.")
            gameflow_explanation3 = "Even if your player's input style is manual, you can generate random inputs by simply pressing"\
                +" 'Enter'. In fact you can run through the whole game by simply holding 'Enter'."
            print("\n" + gameflow_explanation3 + "\n")
            
            input(">> Press 'Enter' to start the game.")
        str2 = str0 + "######################"
        start_game = "You are now going to play a game of LUZA. Enjoy, and make sure to beat the bot."
        print("\n" + str2 + "\n" + start_game + "\n" + str2 + "\n")

def choosePlayersMessage():
    nr_players = input(">> Please specify the number of players for this game. Type 1, 2, 3, or 4: ")
    if nr_players not in ['1','2','3','4']:
        print("The game of LUZA is played by 2,3, or 4 players. You can also play alone if you wish.")
        return choosePlayersMessage()
    print(f"This game of LUZA will be played by {nr_players} players.\n")
    return nr_players

def announceThePlayers(game : Game):
    str0 = "This game of LUZA will be played by the following players: \n"
    playastr = ""
    for player in game.players:
        if player.input_style['mechanism']['display'] == 'automatic':
            playastr += f"{player.name} (BOT) \n"
        else:
                playastr += f"{player.name} (Human) \n"
    print(str0 + playastr)