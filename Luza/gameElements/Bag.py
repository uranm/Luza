from gameElements.Tile import Tile
from gameElements.FactoryDisplay import FactoryDisplay, FullDisplay
import random


## this is the bag that contains all the tiles to be used during the game

class Bag:

    ## the bag has 20 tiles of each color 1,2,3,4,5. It also has the penalty tile,
    ## but we treat that separately.

    def __init__(self, size : int = 100):
        self.tiles = Tile.tilesFromColors([(i%5)+1 for i in range(size)])
    
    ## in case the bag runs out of tiles, we can refill it with the remaining tiles
    def refillBag(self,tiles : list):
        self.tiles += tiles

    ## we try to fill a Factory Display with 4 tiles at most.
    def fillFactoryDisplay(self,fd : FactoryDisplay):
        i = 0
        while i < 4 and (len(self.tiles) > 0) and (len(fd.tiles) <4):
            random_index = random.choice(range(len(self.tiles)))
            fd.addTile(self.tiles.pop(random_index))
            i += 1
    
    ## filling all the Factory Displays in the Full Display
    def fillFullDisplay(self, fullDisplay : FullDisplay):
        for key, display in fullDisplay.displays.items():
            if key != 'C':
                self.fillFactoryDisplay(display)
            if key == 'C' and len(display.tiles) == 0:
                display.fillFactory()
        
    ## check if the bag is empty
    def isEmpty(self):
        return True if len(self.tiles) == 0 else False
    
    ## print the bag contents
    def __str__(self):
        tile_colors = tuple(Tile.tileColors(self.tiles))
        one_tiles = tile_colors.count(1)
        two_tiles = tile_colors.count(2)
        three_tiles = tile_colors.count(3)
        four_tiles = tile_colors.count(4)
        five_tiles = tile_colors.count(5)
        total_tiles = len(tile_colors)

        str1 = str(one_tiles)+"x1"
        str2 = str(two_tiles)+"x2"
        str3 = str(three_tiles)+"x3"
        str4 = str(four_tiles)+"x4"
        str5 = str(five_tiles)+"x5"
        total = "Total tiles: " + str(total_tiles)

        return "Bag contents: \n "+ str1 +", " + str2 + ", " + str3 + ", "+ str4 + ", " + str5 +"\n"+total 

