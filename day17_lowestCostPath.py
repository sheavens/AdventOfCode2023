""" Find the lowest cost path from top left to bottom right of a grid of numbers,
where only 3 consecutive moves in the same direction are allowed.
In part 2 a minimum of 4 moves in the same direction is required, and a maximum of 10
allowed before turning. """

from queue import PriorityQueue

testData = [
'2413432311323',
'3215453535623',
'3255245654254',
'3446585845452',
'4546657867536',
'1438598798454',
'4457876987766',
'3637877979653',
'4654967986887',
'4564679986453',
'1224686865563',
'2546548887735',
'4322674655533',
]

# grid = [[int(c) for c in line] for line in testData]
grid = [[int(c) for c in line] for line in open('day17_input.txt').read().splitlines()]

def manhatten(position, target):
    return abs(position[0] - target[0]) + abs(position[1] - target[1])

def onGrid(position, grid):
    # returns true if the position is on the grid
    row, col = position
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0])
 
def next(fromHere, directions, grid):
    position, cumCost, entryPath = fromHere
    # return the tuple of position, cumcost and entry path of next moves to positions that are on the grid
    nextMoves = []
    dirs = []
    for d in directions :
        if d == '>' :
            x, y = position[0]+1, position[1]
            dirs.append(((x,y),d))
        elif d == 'v' :
            x, y = position[0], position[1]+1
            dirs.append(((x,y),d))
        elif d == '<' :
            x, y = position[0]-1, position[1]
            dirs.append(((x,y),d))
        elif d == '^':
            x, y = position[0], position[1]-1
            dirs.append(((x,y),d))
        else :
            print('Unknown direction', d)
    return [((x, y), cumCost + grid[y][x], entryPath[1:]+d) for ((x, y),d) in dirs if onGrid((x, y), grid)]
    
def priority(position, grid, target) :
    return manhatten(position, target) + grid[position[0]][position[1]]  # use manhatten plus heat loss as priority

def nextMoves(fromHere, grid) :
    # return a list of the next moves to try; no more than 3 moves in the same direction are allowed

    _, _, entryPath = fromHere   # entryPath is a string of the last 3 entry directions taken e.g 'v>>'
    direction = entryPath[-1] # the direction from which we arrived here
    allDirections = ['<','>','^','v']
    reverse = {'<':'>', '>':'<', '^':'v', 'v':'^'}
    if direction in allDirections:
        nextDirs = [d for d in allDirections if direction and d != reverse[direction]] # every way except backwards
    else:
        nextDirs = allDirections

    if len(entryPath) > 2 and entryPath[-1] == entryPath[-2] == entryPath[-3]:
        nextDirs = [d for d in nextDirs if d != entryPath[-1]] # can't make more than three moves in the same direction   
    
    return next(fromHere, nextDirs, grid)

def solveItPart1(grid) :
    # a priority queue of moves to try next, ordered by lowest cost + heuristic (manhatten distance)
    moves = PriorityQueue()  
    # add the start positon to the queue; 
    # store tuple of position, cum cost to here and last 3 entry directions (as a string or arrows) 
    start = ((0,0), 0, '...') # No cumcost for start, and no entry path (3 '.' characters stored instead). 
    moves.put((0, start)) # priority 0 for start position

    target = (len(grid)-1, len(grid[0])-1) # end position
    visited = set() # a set to hold visited grid positions

    while moves.qsize() > 0:
        _, move = moves.get()
        # make the next move in the queue
        here, cumCost, entryPath = move

        if (here, entryPath) in visited: # ignore any positions already visited
        # both the position and the last 3 entry directions are stored in the visited set
        # - because the next movement option differ accoring to last 3 entry steps 
        # (cannot make more than 3 moves in the same direction)
            continue 
        visited.add((here, entryPath))

        if here == target:
            return cumCost # lowest cost path found 
        
        toThere = nextMoves(move, grid)
        for choice in toThere:
            toPosition, cumCostThere, _ = choice
            moves.put((cumCostThere + manhatten(toPosition, target), choice))
            # it could be that the same position and entry is added to the queue more than once, but with different cumCosts
            # the PriorityQueue will always return the lowest cost first, so the first time it is dequeed is the lowest cost path to that position
            # .. and the next time will be ignored as it is in visited set.


def nextPart2(fromHere, nextSteps, grid):
    position, cumCost, entryPath = fromHere
    # return the tuple of position, cumcost and entry path of next moves to positions that are on the grid
    nextMoves = []
    x0, y0 = position[0], position[1]

    for step in nextSteps :
        # step will be strings of 4 to 10 of same arrow ('>,^,v,^) characters, meaning 4 to 10 steps in that direction
        d = step[-1]
        if d == '>' :
            xInc = 1
            yInc = 0
        elif d == 'v' :
            xInc = 0
            yInc = 1
        elif d == '<' :
            xInc = -1
            yInc = 0
        elif d == '^':
            xInc = 0
            yInc = -1 
        blocks = len(step)
        offGrid = True
        cc = cumCost
        x = x0
        y = y0
        ePathList = [c for c in entryPath]
        for b in range(blocks): # adds the cost of 4 to 10 blocks as 1 move
            x += xInc
            y += yInc
            if onGrid((x, y), grid):
                offGrid = False
                cc = cc + grid[y][x]
                ePathList[-b-1] = d             
            else:
                break # have gone off the grid so move to next
        if not offGrid : # there will be no moves if all nextSteps are off the grid
            nextMoves.append(((x,y),cc, ''.join(ePathList)))
    return nextMoves

def priority(position, grid, target) :
    return manhatten(position, target) + grid[position[0]][position[1]]  # use manhatten plus heat loss as priority

def nextMovesPart2(fromHere, grid) :
    # return a list of the next moves to try; at least 4 and no more than 10 moves in the same direction are allowed

    _, _, entryPath = fromHere   # entryPath is a string of the last 3 entry directions taken e.g 'v>>'
    direction = entryPath[-1] # the direction from which we arrived here
    allDirections = ['<','>','^','v']
    reverse = {'<':'>', '>':'<', '^':'v', 'v':'^'}
    if direction in allDirections:
        # not backwards and cannot leave in same direction because all moves (4 to 10) in that direction have been tried
        nextDirs = [d for d in allDirections if d != reverse[direction] and d!=direction] 
    else:
        nextDirs = allDirections
    # extend the extry path to 4 to 10 steps in the same drection
    nextSteps = []
    for direction in nextDirs:
        for d in range(4,11):
            nextSteps.append(direction*d)
  
    return nextPart2(fromHere, nextSteps, grid)

def solveItPart2(grid) :
    # For Part 2 must make a minimum of four moves in the same  direction, 
    # and no more than 10 before turning.

    # a priority queue of moves to try next, ordered by lowest cost + heuristic (manhatten distance)
    moves = PriorityQueue()  
    # add the start positon to the queue; 
    # store tuple of position, cum cost to here and last 3 entry directions (as a string or arrows) 
    start = ((0,0), 0, '..........') # No cumcost for start, and no entry path (10 '.' characters stored instead). 
    moves.put((0, start)) # priority 0 for start position

    target = (len(grid)-1, len(grid[0])-1) # end position
    visited = set() # a set to hold visited grid positions

    while moves.qsize() > 0:
        _, move = moves.get()
        # make the next move in the queue
        here, cumCost, entryPath = move

        if (here, entryPath[-1]) in visited: # ignore any positions already visited
        # In this version all moves in from a given direction are the same for visited set,
        # whether coming 4 or 10 prior steps in that direction, because all the
        # moves out of any block have been added to the queue and prioritised..
        # any return here from those moves will be at higher cost and can be ignored.
        # This change allowed Part 2 to be solved in a reasonable time.

            continue 
        visited.add((here, entryPath[-1]))

        if here == target:
            return cumCost # lowest cost path found 
        
        toThere = nextMovesPart2(move, grid)
        for choice in toThere:
            toPosition, cumCostThere, _ = choice
            moves.put((cumCostThere + manhatten(toPosition, target), choice))

# print('Part1 : ', solveItPart1(grid))   
print('Part2 : ', solveItPart2(grid))
