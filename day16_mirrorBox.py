
""" Find cells energised by beams of light crossing them.  
Beams are split into two by 'splitters' or deflected by mirrors in the grid.
Part 1 find the number of cells energised by starting the beam at the top left corner of the grid, facing right
Part 2 find the largest number of cells energised by starting the beam at any entry point on the sides of the grid, heading inwards """

import queue

testData = [
    '.|...\\....',
    '|.-.\\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....',
]

#grid = [[ c for c in line ] for line in testData]
grid = [[ c for c in line ] for line in open('day16_input.txt', 'r').read().splitlines()]

# travesre the grid until a mirror or splitter reached, collecting the coordinates of the cells and the entered in a set of tuples
# if the set already contains the coordinates and direction, can end tracking; all future entries will be duplicates
# if a splitter is reached, end the beam, queue two beams, one in each direction
# if a mirror is reached, change the direction of travel
# if beam exits the grid, end the beam
# when all beams have exited the grid, return the size of the set of tuples

def onGrid(coords, grid):
    x, y = coords
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def moveBeamlet(beamlet, grid):
    (row, col), direction = beamlet
    if direction == '>':
        col += 1
    elif direction == '<':
        col -= 1
    elif direction == '^':
        row -= 1
    elif direction == 'V':
        row += 1
    else :
        print('invalid direction : ', direction)
    return ((row, col), direction)


# experimenting with arrow symbols for recording direction...
arrowDict = { '>' : {'|': ['^', 'V'], '\\': ['V'], '/': ['^'], '-': ['>']},
              '<' : {'|': ['^', 'V'], '\\': ['^'], '/': ['V'], '-': ['<']},
              '^' : {'-': ['<', '>'], '\\': ['<'], '/': ['>'], '|': ['^']},
              'V' : {'-': ['<', '>'], '\\': ['>'], '/': ['<'], '|': ['V']} }

def energiseTiles(startBeamlet, grid):
    # start at the top left corner of the grid, facing right

    beamlet = startBeamlet
    beamletSet = set() # keep a set of beam particles with coordinates and direction
    coordsSet = set() # keep a set of coordinates of beam particles
    beamletQ = queue.Queue() # queue the active beam particles
    beamletQ.put(beamlet)

    # while the beam is on the grid, move beamlet
    while not beamletQ.empty():
        beamlet = beamletQ.get() # process the next beamlet

        if beamlet in beamletSet: # !!! I suspect this step is saving a lot of time in part 2
            continue  # beamlet path has already been tracked so no new cells will be covered
        
        coords, direction = beamlet
        while onGrid(coords, grid) : # keep moving until beamlet leaves grid
            beamletSet.add(beamlet)
            coordsSet.add(coords)
            x, y = coords 
            if grid[x][y] == '.': # empty cell, keep moving 
                beamlet = moveBeamlet(beamlet, grid)
                coords, direction = beamlet
                # x, y = coords
            else: # has hit a mirror or splitter
                dict = arrowDict[direction]
                newDirections = dict[grid[x][y]]
                for dir in newDirections:
                    newBeamlet = (coords, dir)
                    beamletQ.put(moveBeamlet(newBeamlet, grid)) # move on and queue the new beamlets from here
                break

    return len(coordsSet)

# Part 1 find the number of cells energised by starting the beam at the top left corner of the grid, facing right
print('Part 1 : ', energiseTiles( ((0,0), '>'), grid))

#Part 2 find the largest number of cells energised by starting the beam at any entry point on the sides of the grid, heading inwards

topEdge = [((0, col), 'V') for col in range(len(grid[0]))]
leftEdge = [((row, 0), '>') for row in range(len(grid))]
bottomEdge = [((len(grid)-1, col), '^') for col in range(len(grid[0]))]
rightEdge = [((row, len(grid[0])-1), '<') for row in range(len(grid))]

entryBeams = topEdge + leftEdge + bottomEdge + rightEdge
# test all possible entry points on the sides of the grid

largestEnergisedTiles = 0
for i, beamlet in enumerate(entryBeams):
    energised  =  energiseTiles(beamlet, grid)
    if energised > largestEnergisedTiles:
        # print(energised, i)
        largestEnergisedTiles = energised
 
print('Part 2 : ', largestEnergisedTiles)
