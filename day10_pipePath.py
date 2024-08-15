# Given a pattern of pipes, being horizontal, vertical or corner pieces.
# Part 1, find the number of steps to reach the furthest point in the path opf pipes.
# Part 2, find the number of enclosed cells in the path of pipes which form a colosed loop.

import queue
import copy

testInput = [
'..F7.',
'.FJ|.',
'SJ.L7',
'|F--J',
'LJ...',
]

testPart2Input = [
'..........',
'.S------7.',
'.|F----7|.',
'.||....||.',
'.||....||.',
'.|L-7F-J|.',
'.|..||..|.',
'.L--JL--J.',
'..........',
]

testPart2Input2 = [
'.F----7F7F7F7F-7....',
'.|F--7||||||||FJ....',
'.||.FJ||||||||L7....',
'FJL7L7LJLJ||LJ.L-7..',
'L--J.L7...LJS7F-7L7.',
'....F-J..F7FJ|L7L7L7',
'....L7.F7||L7|.L7L7|',
'.....|FJLJ|FJ|F7|.LJ',
'....FJL-7.||.||||...',
'....L---J.LJ.LJLJ...',
]

testGridInput3 = [
'FF7FSF7F7F7F7F7F---7',
'L|LJ||||||||||||F--J',
'FL-7LJLJ||||||LJL-77',
'F--JF--7||LJLJ7F7FJ-',
'L---JF-JLJ.||-FJLJJ7',
'|F|F-JF---7F7-L7L|7|',
'|FFJF7L7F-JF7|JL---7',
'7-L-JL7||F7|L7F-7F7|',
'L.L7LFJ|||||FJL7||LJ',
'L7JLJL-JLJLJL--JLJ.L',
]

testGrid = [[c for c in line] for line in testGridInput3] 
input = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]
grid = [[c for c in line] for line in input('day10_input.txt')] 

def newLoc(loc, direction) : 
    row, col = loc
    # assumes new loaction is on the grid
    if direction == 'N' :
        return (row-1, col)
    elif direction == 'S' :
        return (row+1, col)
    elif direction == 'E' :
        return (row, col+1)
    elif direction == 'W' :
        return (row, col-1)
    else :
        return 'Error, invalid direction'

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
southPipes = ['|','L','J'] # allow a nove to the south.
northPipes = ['|','7','F']
westPipes = ['-','L','F']
eastPipes = ['-','J','7']

pipe_dict = {'|': ['N','S'], '-':['E','W'], 'L':['N','E'], 'J':['N','W'], '7':['S','W'], 'F':['S','E']}
moveTo = lambda fr, pipe : pipe_dict.get(pipe)[0] if fr is pipe_dict.get(pipe)[1] else pipe_dict.get(pipe)[1]
arrow_Dict = {'N':'^', 'S':'v', 'E':'>', 'W':'<'}

def north(loc, grid_dict):
    row, col = loc
    return grid_dict.get((row -1, col))
 
def south(loc, grid_dict):
    row, col = loc
    return grid_dict.get((row + 1, col))

def east(loc, grid_dict):
    row, col = loc
    return grid_dict.get((row, col + 1))

def west(loc, grid_dict):
    row, col = loc
    return grid_dict.get((row, col - 1))

isNS = lambda loc, grid_dict : north(loc, grid_dict) in northPipes and south(loc, grid_dict) in southPipes
isEW = lambda loc, grid_dict : east(loc, grid_dict) in eastPipes and west(loc, grid_dict) in westPipes
isNE = lambda loc, grid_dict : north(loc, grid_dict) in northPipes and east(loc, grid_dict) in eastPipes
isNW = lambda loc, grid_dict : north(loc, grid_dict) in northPipes and west(loc, grid_dict) in westPipes
isSW = lambda loc, grid_dict : south(loc, grid_dict) in southPipes and west(loc, grid_dict) in westPipes
isSE = lambda loc, grid_dict : south(loc, grid_dict) in southPipes and east(loc, grid_dict) in eastPipes

def get_startPipe(loc, grid_dict) :
    # print(north(loc, grid_dict), south(loc, grid_dict), east(loc, grid_dict), west(loc, grid_dict))
    if isNS(loc, grid_dict) :
        return '|'
    elif isEW(loc, grid_dict) :
        return '-'
    elif isNE(loc, grid_dict) :
        return 'L'
    elif isNW(loc, grid_dict) :
        return 'J'
    elif isSW(loc, grid_dict) :
        return '7'
    elif isSE(loc, grid_dict) :
        return 'F'
    else :
        return 'Error, no pipe found at start location.'


oppositeDirection = lambda direction : 'N' if direction == 'S' else 'S' if direction == 'N' else 'E' if direction == 'W' else 'W'

def getPath(gridLocs, grid_dict, grid) :
    
    pathMap = copy.deepcopy(grid)
    path = []

    startLoc = [(row,col) for row, col in gridLocs if grid[row][col] == 'S'][0]
    # determine which type of pipe we are starting on
    startPipe = get_startPipe(startLoc, grid_dict)
    grid_dict[startLoc] = startPipe # overwrite the start location with the pipe type
    loc = startLoc
    path.append(loc)
    # pipe = get_startPipe(loc, grid)
    fr = pipe_dict.get(startPipe)[0] # the direction we are coming from (could choose eith end of the start pipe)
    to = pipe_dict.get(startPipe)[1]
    # make the first move
    loc = newLoc(loc, to)
    pipe = grid_dict.get(loc) # get the pipe we are on
    path.append(loc)
    fr = oppositeDirection(to)
    while (loc != startLoc) :
        pathMap[loc[0]][loc[1]] = arrow_Dict[fr]
        to = moveTo(fr, pipe)
        loc = newLoc(loc, to)
        pipe = grid_dict.get(loc) # get the pipe we are on
        path.append(loc)
        fr = oppositeDirection(to)
    pathMap[loc[0]][loc[1]] = arrow_Dict[fr] # overwrite the start location wth the direction.
    return path, pathMap

def solveItPart1(grid):
    # part 1 - the number of steps to reach the furthest point in the path of pipes is
    # just half the length of the path.
    gridLocs = [(row,col) for row in range(len(grid)) for col in range(len(grid[0]))]
    flatGrid = [grid[row][col] for row in range(len(grid)) for col in range(len(grid[0]))]
    grid_dict = dict(zip(gridLocs, flatGrid)) # a dictionary of values looked up from (row,col) tuples :
    path, _ = getPath(gridLocs, grid_dict, grid)
    return len(path) / 2

print('Part 1: ', solveItPart1(grid)) # 7063

# Part  2:
def printGrid(grid) :
    for row in range(len(grid)) :
        for col in range(len(grid[0])) :
            print(grid[row][col], end='')
        print()

def printOnGrid(grid, coordSet, char) :
    for row in range(len(grid)) :
        for col in range(len(grid[0])) :
            if (row, col) in coordSet :
                print(char, end='')
            else :
                print(grid[row][col], end='')
        print()

def printPath(path) :
    order = range(len(path))
    pathOrder = dict(zip(path, order))
    for row in range(len(grid)) :
        for col in range(len(grid[0])) :
            if (row,col) in path :
                print('X', end='')
            else :
                print('.', end = '')
        print()

def neighbours(cell):
    row, col = cell
    return [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

def floodfill(coordSet, innerCell, boundaryList):
    q = queue.Queue()
    # floodfill empty from this inner cell, with boundary
    if innerCell not in coordSet and innerCell not in boundaryList:  # if this innercell is in the coordset, this inner area has already been filled
        coordSet.add(innerCell)
        q.put(innerCell)
        while not q.empty():
            innerCell = q.get()
            for n in neighbours(innerCell):
                if n not in coordSet and n not in boundaryList:
                    coordSet.add(n)
                    q.put(n)
    # print(len(coordSet))
    return coordSet

def determine_direction(cell, nextCell):
    row, col = cell
    nextRow, nextCol = nextCell
    if nextCol - col == 1:
        direction = 'E'
    elif nextCol - col == -1:
        direction = 'W'
    elif nextRow - row == 1:
        direction = 'S'
    else:
        direction = 'N'
    return direction

def getInnerCell(cell, direction, clockwise):
    # innercell is to the right of the direction of travel for clockwise
    row, col = cell
    if clockwise:
        if direction == 'N':
            return (row, col + 1)
        elif direction == 'E':
            return (row + 1, col)
        elif direction == 'S':
            return (row, col - 1)
        elif direction == 'W':
            return (row - 1, col)
    else:
        if direction == 'N':
            return (row, col - 1)
        elif direction == 'E':
            return (row - 1, col)
        elif direction == 'S':
            return (row, col + 1)
        elif direction == 'W':
            return (row + 1, col)
 
def getEnclosedCells(boundary):
    if boundary[0] == boundary[len(boundary)-1]:
        boundary.pop() # remove the last cell, as it is the same as the first
        print('boundary is not now a loop')
    # boundary.append(boundary[0]) # make it a loop   !! ToDo maight not want this
        

    # fill in the enclosed cells
    # boundary could be convoluted and a cell could be on both boundaries.
    # 
    # if travelling clockwise around the boundary, inner cells are to the right of the direction of trave.
    # The cell with the leftmost column will be on the leftmost boundary.   Going to the North (or East)
    # will be clockwise.

    # find the leftmost edge on the boundary
    minCol = min(col for row, col in boundary)        
    leftEdge = [(row, col) for row, col in boundary if col == minCol]
    # From an edge cell, go around the boundary, finding the inner cels along the boundary wall
    startCell = leftEdge[0]
    index = boundary.index(startCell)
    boundary = boundary[index:] + boundary[:index]  # make the start cell the first in the list
    # add the start cell to the end of the list, so we can loop around
    boundary.append(boundary[len(boundary)-1]) #!! made no difference ..
    next = boundary[1]
    direction = determine_direction(startCell, next)
    # if the next cell is to the North or East of the start cell, we are going clockwise
    if direction == 'N' or direction == 'E':
        clockwise = True
    else:
        clockwise = False
    # traverse the boundary, finding the inner cells along the boundary wall
    innerCells = []
    for index in range(len(boundary)-1):
        cell = boundary[index]
        next = boundary[index+1]
        direction = determine_direction(cell, next)
        innercell = getInnerCell(cell, direction, clockwise)
        if innercell not in boundary:
            innerCells.append(innercell)

    coordSet = set()
    for innerCell in innerCells:
        # floodfill empty cells from this inner cell, within boundary loop
        coordSet = floodfill(coordSet, innerCell, boundary)
        # although all cells might be found in the first floodfill.. 
        # if the boundary walls touch, they may be separate areas to find, so test using all cells next to the boundary
            
    return coordSet

 # Part 2 attempted solution using flood-fill of a connected area, having identified an enclosed cell (between the boundary walls).   
def countEnclosedCells2(boundary):
    if boundary[0] != boundary[len(boundary)-1]:
        print('Error: boundary is not a loop')
        boundary.append(boundary[0]) # make it a loop
    # fill in the enclosed cells
    # boundary could be convoluted and a cell could be on both boundaries.
    # 
    # if travelling clockwise around the boundary, inner cells are to the right of the direction of trave.
    # The cell with the leftmost column will be on the leftmost boundary.   Going to the North (or East)
    # will be clockwise.

    # find the leftmost edge on the boundary
    minCol = min(col for row, col in boundary)        
    leftEdge = [(row, col) for row, col in boundary if col == minCol]
    # From an edge cell, go clockwise around the boundary, finding the inner cels along the boundary wall
    startCell = leftEdge[0]
    clockwise = []
    row, col = startCell
    # Clockwise cell is North or East of starting left edge cell

    if (row-1, col) in boundary:
        direction = 'N'
        nextCell = (row-1, col)
    elif (row, col+1) in boundary:
        direction = 'E'
        nextCell = (row, col+1)
    else:
        print('Error: no boundary cell to the North or East of the leftmost edge cell')

    # from a given heading can go to the next boundary cell in these directions (erxcludes reverse direction)  
    fromHereDict = {'N': ['N', 'E', 'W'], 'E' : [ 'E', 'N', 'S'], 
                    'S': ['S', 'E', 'W'], 'W': ['W', 'N', 'S']} 
      
    innerCells = []
    i = 0
    while nextCell != startCell:
        i += 1
        if i > len(boundary):
            print('Error: boundary loop not found')
            break

        for dir in fromHereDict[direction]: # try each direction in turn to find next clockwise boundary cell
            if dir == 'N':
                innerCell = (row, col+1)
                nextCell = (row-1, col)
            elif dir == 'E':
                innerCell = (row+1, col)
                nextCell = (row, col+1)
            elif dir == 'S':
                innerCell = (row, col-1)
                nextCell = (row+1, col)
            elif dir == 'W':
                innerCell = (row-1, col)
                nextCell = (row, col-1)
            if nextCell in boundary:
                direction = dir
                if innerCell not in boundary:
                    innerCells.append(innerCell)
                clockwise.append(nextCell) # will add the startCell at the end
                row, col = nextCell
                break
    
    coordSet = set()
    for innerCell in innerCells:
        # floodfill empty cells from this inner cell, within boundary loop
        coordSet = floodfill(coordSet, innerCell, clockwise)
        # although all cells might be found in the first floodfill.. 
        # if the boundary walls touch, they may be separate areas to find, so test using all cells next to the boundary
            
    # return the number of squares filled
    # printGrid(coordSet)
    return len(coordSet)


# try a different approach.
# count the number of times the boundary is crossed before reaching a cell.
# in, cell, out  - the cell is enclosed if an odd number of crossings occur before reaching in.

# answer was 589, solved by this 'ray-casting' approach. 
# The flood-fill approach was 2 out (don't know why), but all test cases worked - annoying when that happens!
#
def solvitPart2(grid) :
    gridLocs = [(row,col) for row in range(len(grid)) for col in range(len(grid[0]))]
    flatGrid = [grid[row][col] for row in range(len(grid)) for col in range(len(grid[0]))]
    grid_dict = dict(zip(gridLocs, flatGrid)) # a dictionary of values looked up from (row,col) tuples
    path, pathMap = getPath(gridLocs, grid_dict, grid)
    startLoc = [(row,col) for row, col in gridLocs if grid[row][col] == 'S'][0]
    # determine which type of pipe we are starting on
    startPipe = get_startPipe(startLoc, grid_dict)
    grid_dict[startLoc] = startPipe # overwrite the start location with the pipe type
    grid[startLoc[0]][startLoc[1]] = startPipe
    # printGrid(pathMap)
    count = 0
    for row in range(len(grid)):
        enclosed = False
        firstOfPair = True
        for column in range(len(grid[0])):
            if (row,column) in path: 
                cell = grid_dict.get((row,column)) # have made grid_dict (row, column)
                if cell == '-' :
                    continue # ignore horizontal wall in line
                elif cell == '|':
                    enclosed = not enclosed # passed through a single vertical wall - switch enclosed status
                elif cell in ['F','J','7','L']:
                    if firstOfPair:
                        first = cell
                        firstOfPair = False
                        enclosed = not enclosed # passed through a 90 degree bend - switch enclosed status
                    else: # other letter pairings to those below are equivalent to single vertical wall and do not switch enclosed status
                        if first in ['L','J'] and cell in ['L','J'] \
                            or first in ['7','F'] and cell in ['7','F']:
                            enclosed = not enclosed
                        firstOfPair = True
            elif enclosed: # if not on the path, but enclosed, count the enclosed cells
                count += 1

    # printOnGrid(grid, path, '#')
    # enclosed = getEnclosedCells(path)  - this gave 587 
    # printOnGrid(pathMap, enclosed, '@')
    return count # len(enclosed)

print('Part 2 :' , solvitPart2(grid)) # 589 - correct answer









