#%%
from Game import Game
from interactiveMessages.GameFlowMessages import beginningOfGameMessage, choosePlayersMessage, announceThePlayers
#%%

beginningOfGameMessage()
nr_players = choosePlayersMessage()
g = Game(int(nr_players))
g.enterPlayerDetails()
announceThePlayers(g)
g.play()
g.endOfGameMessage()
