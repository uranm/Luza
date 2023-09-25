from abc import ABC
from gameElements.Tile import Tile

#%%
## generic picking zone, can be either a factory display, or the middle display.

class PickZone(ABC):
    def __init__(self,name : str):
        self.name = name
        self.tiles = []

    ## returns all the tiles of a given color after removing them from a pick zone
    def pickTilesOfColor(self,color : int):
        pickedTiles = []
        selftiles_temp = []
        if color not in [tile.color for tile in self.tiles]:
            raise ValueError("That color is not available")
        for tile in self.tiles:
            if tile.color == color:
                pickedTiles.append(tile)
            else:
                selftiles_temp.append(tile)
        if len(pickedTiles) == 0:
            print("The color %d is not in the display." %color)
            return []

        self.tiles = selftiles_temp    
        return pickedTiles
    
    ## fills the factory displays (not the center) with 4 tiles of random colors,
    ## implemented below for the class FactoryDisplay. The center is filled
    ## with the penalty tile of color 0 (marked 1 in Azul)
    def fillFactory(self):
        pass
    
    ## add a single tile to the Pick Zone
    def addTile(self,tile : Tile):
        self.tiles.append(tile)
    
    ## adds a list of tiles to the Pick Zone
    def addTiles(self, tiles : list):
        for tile in tiles:
            self.addTile(tile)

    ## removes and returns all the tiles from the Pick Zone
    def clear(self):
        tiles_temp = self.tiles
        self.tiles = []
        return tiles_temp

    ## prints the name of the Pick Zone and its colors
    def __str__(self):
        return self.name+ " " + f"{Tile.p(self.tiles)}"
#%%
## instance of Pick Zone. These are the factory displays, or circles, in Azul
## that hold tiles.

class FactoryDisplay(PickZone):
    def __init__(self,name : str):
        super().__init__(name)
    
    def fillFactory(self, tiles : list):
        if len(self.tiles) == 0 and len(tiles) == 0:
            self.addTiles(tiles)
        else:
            raise ValueError("Your factory display is either not empty, or you are attempting to fill\
                             it with more than 4 tiles.")

#%%

## instance of PickZone. This is the central display in Azul. At the start of 
## each round it holds only the penalty tile, and later all unpicked tiles from the
## Factory Displays are deposited here.

class CenterDisplay(PickZone):
    def __init__(self, name : str = 'CTR'):
        super().__init__(name)
        self.tiles = []
        self.penaltyTile = True ## boolean to keep track of the penalty tile's presence
    
    def pickPenaltyTile(self):
        if self.penaltyTile:
            self.penaltyTile = False
            return super().pickTilesOfColor(0)
        return []

    def pickTilesOfColor(self,color : int):
        picked_tiles = []
        if color == 0:
            return self.pickPenaltyTile()
        
        picked_tiles = super().pickTilesOfColor(color)
        picked_tiles += self.pickPenaltyTile()
        return picked_tiles
    
    ## The next method is used at the start of each round
    def fillFactory(self):
        self.addTiles([Tile(0)])
        self.penaltyTile = True
#%%

## This class consists of all the displays: Factories and Center

class FullDisplay():
    def __init__(self, nr_of_displays : int):
        self.nr_of_displays = nr_of_displays
        self.displays = dict()
        for i in range(self.nr_of_displays):
            self.displays['FD'+str(i+1)] = FactoryDisplay('FD'+str(i+1))
        self.displays['C'] = CenterDisplay('CTR')
    
    ## pick tiles of a given color from a given display
    def pickTiles(self, display_name : str, color : int):

        try:
            display = self.displays[display_name]
        except KeyError:
            print("That display does not exist. Try one of "+f"{[key for key in self.display.keys()]}]")

        pickedTiles = display.pickTilesOfColor(color)
        # remaining_tiles = display.tiles

        ## if you pick from a factory tile, dispose the rest of the tiles to the center
        if isinstance(display,FactoryDisplay):
            cc = self.displays['C']
            remaining_tiles = display.clear()
            cc.addTiles(remaining_tiles)
        
        if pickedTiles == []:
            raise ValueError("You haven't picked any tiles")
        return pickedTiles
    
    ## check if the Full Display is empty
    def isEmpty(self):
        return not self.numberOfTiles()
    
    # get the number of tiles on display
    def numberOfTiles(self):
        total = 0
        for key, value in self.displays.items():
            total += len(value.tiles)
        return total

    ## clear all the tiles from the Full Display
    def clear(self):
        for key, value in self.displays.items():
            value.clear()
    
    def __str__(self):
        result = "Full Display \n"

        for key, display in self.displays.items():
            result += display.__str__()
            result += "\n"
        
        return result

    