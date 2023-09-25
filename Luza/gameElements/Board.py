from abc import ABC
from gameElements.Tile import Tile
from gameElements.Scoring import computeBlockBuildScore, lineBonuses, columnBonuses, colorBonuses
from tabulate import tabulate
## this is a generic line of the board where we place tiles

class Line(ABC):
    def __init__(self, length : int):
        self.length = length
        self.entries = []

    ## main utility of the line is that we place tiles on it. This method
    ## places tiles on a line, and returns those that couldn't be placed due
    ## to length constraints.
    def placeTiles(self,tiles):
        if len(tiles) == 0:
            return
        while len(self.entries) < self.length and len(tiles) >0:
            self.entries.append(tiles.pop())
        return tiles
    
    ## removes and returns all the entries of a line
    def clearLine(self):
        self_entries_temp = self.entries
        self.entries = []

        return self_entries_temp

    # return a boolean to signify if the line is completed
    def isComplete(self):
        if len(self.entries) == self.length:
            return True
        return False
    
    ## is implemented for FloorLine
    def computeScore(self):
        pass
    ## returns the colors of the entries in a line. Normally they should all be
    ## of the same color.
    def __str__(self):
        return f"{Tile.tileColors(self.entries)}"

## this is the floor line, where we place tiles that could not otherwise be placed
## on the regular lines (see below)

class FloorLine(Line):
    def __init__(self):
        super().__init__(7)
        self.coefficients = [-1,-1,-2,-2,-2,-3,-3] # penalty coefficients
    
    # compute the negative score contributed by the floor line
    def computeScore(self):
        number_of_entries = len(self.entries)
        score = sum(self.coefficients[:number_of_entries])
        return score

    # check if 0 is on the floor
    def checkFor0(self):
        for tile in self.entries:
            if tile.color == 0:
                return True
        return False
    # clears the floor line, returning everything except the 0 tile
    def clearLine(self):
        clearedTiles = super().clearLine()

        return [tile for tile in clearedTiles if tile.color != 0]

## this is a regular line where we place tiles of given colors, stored in the
## field .color. Its length should be in [1,...,5].

class RegularLine(Line):
    def __init__(self, length : int):
        if 0 < length < 6:
            super().__init__(length)
            self.color = None
        else:
            raise ValueError("This is a Pattern line, so it cannot have length 7. \
                              Try lengths 1,2,3,4,5.")
        
    def placeTiles(self, tiles):
        ## first get rid of the penalty tile if it's in tiles
        tile0 = None
        for tile in tiles:
            if tile.color == 0:
                tiles.remove(tile)
                tile0 = tile
        if len(tiles) == 0:
            print("There are no tiles to place")
            return
        ## determine the color of the tiles
        if len(self.entries) == 0:
            self.color = tiles[0].color
            remaining_tiles = super().placeTiles(tiles)
        elif self.color == tiles[0].color:
            remaining_tiles = super().placeTiles(tiles)
        else:
            remaining_tiles = tiles
        if tile0 is not None:
            remaining_tiles.append(tile0)

        return remaining_tiles
    
    def clearLine(self):
        self.color = None
        return super().clearLine()

## This class consists of all the Regular(Pattern) Lines and the Floor line

class PatternLines:
    def __init__(self):
        self.lines = [RegularLine(i+1) for i in range(5)]
        self.lines.append(FloorLine())

    # placing tiles in a given line
    def placeTilesInLine(self,tiles, line_index : int):
        if Tile.p(tiles) == [0]:
            self.lines[-1].placeTiles([Tile(0)])
            return []
            
        if len(tiles) == 0:
            raise ValueError("There are no tiles place")
        # we place what we can on the regular line
        remaining_tiles = self.lines[line_index-1].placeTiles(tiles) 

        # the rest we place on the floor line      
        self.lines[-1].placeTiles(remaining_tiles)

    # removes and returns all the tiles from the pattern lines from the board
    def clearPatternLines(self):

        remaining_tiles = []
        for line in self.lines:
            remaining_tiles += line.clearLine()
    
    # returns the line indices where we can place a tile of a given color
    def validLinesToPlace(self,color:int):
        line_indices = []
        for i in range(len(self.lines)):
            line = self.lines[i]
            if isinstance(line,FloorLine):
                # line_indices.append(i)
                pass
            elif line.color is None:
                line_indices.append(i+1)
            elif not line.isComplete() and line.color == color:
                line_indices.append(i+1)
        return line_indices

    # get all tiles on the pattern lines
    def getAllTiles(self):
        all_tiles = []
        for line in self.lines:
            all_tiles += line.entries
        return all_tiles
    
    # number of tiles on pattern lines
    def numberOfTiles(self):
        total = 0
        for line in self.lines:
            total += len(line.entries)
        return total
    ## print the pattern lines
    def __str__(self):
        colors = [Tile.p(self.lines[i].entries) for i in range(6)]
        return f"1. {colors[0]} \n2. {colors[1]} \n3. {colors[2]} \n4. {colors[3]} \n5. {colors[4]} \nF. {colors[5]}"
        

## this is the wall where we place the tiles from completed pattern lines 

class Wall:
    def __init__(self, type : str = 'standard'):
        self.gameOver = False
        if type == 'standard':
            # self.wall = [[1,2,3,4,5],[5,1,2,3,4],[4,5,1,2,3],
            #              [3,4,5,1,2],[2,3,4,5,1]]
            self.wall = [[1,2,3,4,5],[2,3,4,5,1],[3,4,5,1,2],
                         [4,5,1,2,3],[5,1,2,3,4]]
        # this is for the back board, to be implemented later
        if type == 'random':
            pass
    
    # checks if a block of given color has already been built in a given line
    def checkBlockBuild(self, line: int, color : int):
        wall_line = self.wall[line-1]

        if color in wall_line:
            return False
        elif 10*color in wall_line:
            return True
        else:
            return f"The color {color} does not exist."

    # build a block of a given color in a given line of the wall
    def buildBlock(self, line : int, color : int):

        if self.checkBlockBuild(line,color):
            print(f"The block of color {color} in line {line} has already been built.")
            return
        
        wall_line = self.wall[line-1]

        try:
            color_index = wall_line.index(color)
        except ValueError:
            return f"A block of color {color} does not exist."

        wall_line[color_index] *= 10
    
    # checks if any of the lines in the wall have been completed, which signifies
    # the end of the game.
    def isGameOver(self):
        for line in self.wall:
            total = line[0]*line[1]*line[2]*line[3]*line[4]
            if total == 2*3*4*5*100000:
                self.gameOver = True
                return True
        return False
    
    # compute score of building a block of given color in given line
    def computeBlockScore(self, line: int, color : int):
        return computeBlockBuildScore(self,line, color)

    # builds a block in the wall from a given input Pattern Line
    def buildBlockFromLine(self, line : RegularLine):
        if not line.isComplete():
            return f"You cannot build a wall yet, you need %d more block(s)"\
                             "for that" %(line.length-len(line.entries))
        
        wall_line = line.length
        color = line.color
        self.buildBlock(wall_line, color)
        line.entries.pop()

        self.isGameOver()
    
    # compute the bonus scores from the wall
    def computeBonuses(self):
        total_bonuses = lineBonuses(self) + columnBonuses(self) + colorBonuses(self)
        return total_bonuses
    
    # get all tiles on the wall
    def getAllTiles(self):
        all_tiles = []
        for line in self.wall:
            for block in line:
                if block % 10 == 0:
                    all_tiles.append(Tile(int(block / 10)))
        return all_tiles
    
    # number of tiles placed on the wall
    def numberOfTiles(self):
        total = 0
        for line in self.wall:
            for block in line:
                if block % 10 == 0:
                    total += 1
        return total
    # restart the wall
    def restart(self):
        self.wall = [[1,2,3,4,5],[2,3,4,5,1],[3,4,5,1,2],
                         [4,5,1,2,3],[5,1,2,3,4]]
        # self.wall = [[1,2,3,4,5],[5,1,2,3,4]]
        self.gameOver = False
        
    def __str__(self):
        lines = ["","","","",""]
        for i in range(5):
            for j in range(5):
                lines[i] += f"{self.wall[i][j]}   "
        table = self.wall
        return tabulate(table,tablefmt='plain')          
        return f"{lines[0].rjust(5).ljust(5)} \n{lines[1].just(5).rjust(5)} \n{lines[2].ljust(5).rjust(5)}\n{lines[3].rjust(5)} \n{lines[4].ljust(5)}"


## This is a generic board, comprised of the lines where we place tiles, and the
## wall where we build blocks.

class Board:
    def __init__(self,name : str = 'Generic board'):
        self.name = name
        self.patternLines = PatternLines()
        self.wall = Wall()
        self.extraTiles = [] # this will hold the tiles to be removed from the board after each round
        self.score = 0
    
    # check if a tile can be placed in a line
    def canPlaceTilesinLine(self, tiles, line_index: int):
        if len(tiles) == 0:
            # print("There are no tiles to place")
            return True
        
        color = tiles[-1].color
        canPlace = self.wall.checkBlockBuild(line_index,color)

        return not canPlace
    
    # place given tiles on a given line
    def placeTilesInLine(self,tiles : list, line_index : int):
        
        canPlace = self.canPlaceTilesinLine([tile for tile in tiles\
                                              if tile.color != 0],line_index)
        if canPlace:
            self.patternLines.placeTilesInLine(tiles,line_index)
        else:
            self.patternLines.lines[-1].placeTiles(tiles)
        # self.extraTiles += tiles

    # build block in the wall from a line
    def buildBlockFromLine(self, line_index : int):
        line = self.patternLines.lines[line_index-1]
        score = self.wall.computeBlockScore(line_index, line.color)
        self.wall.buildBlockFromLine(line)
        self.score += score
        line_extraTiles = line.clearLine()
        return line_extraTiles

    # build all the blocks possible
    def buildAllBlocks(self):
        for line in self.patternLines.lines[:-1]:
            if line.isComplete():
                extraTiles = self.buildBlockFromLine(line.length)
                self.extraTiles += extraTiles
                
    # update with floor score
    def computeFloorScore(self):
        floor_score = self.patternLines.lines[-1].computeScore()
        temp_score = self.score + floor_score
        if temp_score <=0:
            self.score = 0
        else:
            self.score = temp_score
    
    # get all tiles on the board
    def getAllTiles(self):
        all_tiles = []
        pl_tiles = self.patternLines.getAllTiles()
        wall_tiles = self.wall.getAllTiles()
        xtra_tiles = self.extraTiles

        all_tiles += pl_tiles
        all_tiles += wall_tiles
        all_tiles += xtra_tiles

        return all_tiles

    # number of tiles on the board
    def numberOftiles(self):
        total = self.patternLines.numberOfTiles() + self.wall.numberOfTiles()
        return total
    
    # collect all the extra tiles left on the board
    def clearFloor(self):
        floorTiles = self.patternLines.lines[-1].clearLine()
        self.extraTiles += floorTiles

    # check if 0 is on the floor
    def checkIf0OnFloor(self):
        return self.patternLines.lines[-1].checkFor0()

    # compute bonus scores
    def computeBonuses(self):
        self.score += self.wall.computeBonuses()

    def resetExtraTiles(self):
        self.extraTiles = []

    # print the board
    def __str__(self):              
        str0 = "_____________________________________________"
        pl_rep = "Lines: \n" + self.patternLines.__str__()
        pl_rep_lines = pl_rep.split('\n')

        wall_rep = "Wall: \n" + self.wall.__str__()
        wall_rep_lines = wall_rep.split('\n')
        score = f"Score: {self.score} \n"

        board_view = ""
        for line1, line2 in zip(pl_rep_lines, wall_rep_lines):
            board_view += f"{line1.ljust(30)}{line2}\n"
        board_view += f"{pl_rep_lines[-1]}"

        board_view = str0 + "\n" + "Player: " + self.name\
              +"\n" + score +"\n" + board_view + "\n" + str0
        return board_view

        

    