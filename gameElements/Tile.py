## class that encodes the tile and some generic operations with it

class Tile:
    ## colored tiles are 1 through 5
    ## color 0 is the tile marked 1 in the game, it is unique

    def __init__(self, color : int):
        if 0 <= color <= 5:
            self.color = color
        else:
            raise ValueError("There can't be a tile of color %d. Try 0 <= color <= 5" %color)
    
    ## returns the list of colors of a list of tiles
    @staticmethod
    def tileColors(tiles : list):
        tile_colors = [tile.color for tile in tiles]
        return tile_colors
    
    ## constructs a list of tiles from a list of tile colors
    @staticmethod
    def tilesFromColors(tile_colors : list):
        tiles = []
        for color in tile_colors:
            tiles.append(Tile(color))
        return tiles

    ## prints the color of a tile   
    def __str__(self):
        return f"{self.color}"
    
    ## prints the colors of a list of tiles 
    @staticmethod
    def p(tiles: list):
        return sorted(Tile.tileColors(tiles))

