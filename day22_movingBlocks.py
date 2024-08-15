"""Drop bricks into a pile and then count the number that would fall 
if one brick were removed. Part 1 tests removing one brick, for each in turn
Part 2 allow chain reaction of bricks falling themselves causing more to fall."""

testData = [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9',
]
brickRanges = [line.split('~') for line in testData]

with open('day22_input.txt', 'r') as file:
 brickRanges = [line.split('~') for line in file.read().splitlines()]

input = [[list(map(int, f.split(','))), list(map(int, r.split(',')))] for f, r in brickRanges]

def getBricks(input):
    # returns a list of bricks as a list of lists of tuples of the x,y,z values of each cube in the brick
    bricks = [[] for i in range(len(input))]
    for i, brick in enumerate(input):
        start = brick[0]
        end = brick[1]
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    bricks[i].append((x, y, z))
    return bricks

def commonXY(brick1, brick2):
    # returns true if bricks cover one or more common XY values
    for cube in brick1:
        for cube2 in brick2:
            if cube[0] == cube2[0] and cube[1] == cube2[1]:
                return True
    return False

def getCommonXY(brick, bricks):
    # returns a list of bricks that have common XY values with the brick
    commonXYList = []
    for b in bricks:
        if b is not brick:
            if commonXY(brick, b):
                commonXYList.append(b)
    return commonXYList

def lowestZ(cubes):
    # returns the lowest z value for any cube in the brick
    return min([z for x,y,z in cubes])

def highestZ(cubes):
    # returns the highest z value for any cube in the brick
    return max([z for x,y,z in cubes])

def nextbelow(brick, allFilledCubes):
    # for each cube in the brick, find the highest z value of filled cubes below it
    # excluding cubes in the same brick
    nextBelow = 0
    filledInColumn = []
    for cube in brick:
        cx, cy, cz = cube
        filledInColumn = [z for x,y,z in allFilledCubes if x == cx and y == cy and z < cz if (x,y,z) not in brick]
        nextBelow = max(max(filledInColumn),nextBelow) if len(filledInColumn) > 0 else nextBelow
    return nextBelow 

def bricksInLayerbelow(brick, bricks):
    bricksWithCubeBelow = []
    z = lowestZ(brick)
    for b in bricks:
        zb = highestZ(b)
        if zb == z - 1:
            bricksWithCubeBelow.append(b)
    return bricksWithCubeBelow

def dropBricks2(bricks):
    # More efficient algorithm for dropping bricks
    # bricks is a list of lists of tuples of the x,y,z values of each cube in the brick

    # make a set of the (x,y,z) values of all cubes in all bricks
    allFilledCubes = set()
    allFilledCubes = {cube for brick in bricks for cube in brick}
 
    # sort the bricks by the lowest z value of the cubes in the brick
    bricks.sort(key=lambda x: lowestZ(x))
    fallenBricks = []
    filledBelow = 0
    moves = 0
    for brick in bricks:
        # find the highest filled z value in any (x,y) column below the brick
        filledBelow = nextbelow(brick, allFilledCubes)
        moves = 0
        if lowestZ(brick) > filledBelow + 1:
            # move the brick to the lowest unfilled space available
            moves = lowestZ(brick) - (filledBelow + 1)
            # update allFlledCubes set
            allFilledCubes = allFilledCubes - set(brick)
            allFilledCubes = allFilledCubes.union(set([(x,y,z-moves) for x,y,z in brick]))
        fallenBricks.append([(x,y,z-moves) for x,y,z in brick])
    
    return fallenBricks

def getSupportedBy(bricks) :
    # returns a dictionary of bricks that are suporting each brick
    supportedBy = {}
    for i, brick in enumerate(bricks):
        # store bricks to a set of tuples of the first and last cell in the brick
        key = (brick[0])+(brick[-1])
        supportedBy[key] = []
        # find bricks in commonxy with z value one lower - the supporting bricks
        for b in bricksInLayerbelow(brick, getCommonXY(brick, bricks)):
            supportedBy[key].append(b[0]+b[-1])
    return supportedBy

def getLoneSupported(supportedBy):
    # returns a sert of bricks that are supported by only one other brick
    loneSupporters = set()
    for k, v in supportedBy.items():
        if len(v) == 1:
            loneSupporters.add(v[0])  # add the combined tuple of first and last brick cells to a set
    return loneSupporters

def solveItPart1(input):
    bricks = dropBricks2(getBricks(input)) 
    return (len(bricks) - len(getLoneSupported(getSupportedBy(bricks))))

# Part 2. Chain reaction. Calculated the number of bricks that would fall by removing each og thew bricks.

#.. only the lone supports wil cause another brick or bricks to fall.  
# remove each lone supporter and the then unsupported bricks will fall. It they are lone supporters,
# the chain reaction continues.  Count the bricks that fall in each chain reaction.

def deepCopyDict(d):
    deepCopy = {}
    for k in d.keys(): # needs another layer for lst of lists
        deepCopy[k] = d[k].copy()
        for i, v in enumerate(d[k]):
            deepCopy[k][i] = v
    return deepCopy

def removeBricks(BricksToGo, supportedBy) :
    # returns a list of bricks that will fall if the bricks in BricksToGo are removed
    fallen = []
    deepCopy = deepCopyDict(supportedBy)
    # deepCopy = supportedBy # not a deep copy = wrong answer
    keys = supportedBy.keys()
    for k in keys:
        for b in BricksToGo:
            if b in deepCopy[k]:
                deepCopy[k].remove(b)
                if len(deepCopy[k]) == 0 : # k is only supported by l
                    fallen.append(k)
    # add bricks supported by the fallen bricks
    if len(fallen) > 0:
        fallen = fallen + removeBricks(fallen, deepCopy)               
    return fallen


def solveItPart2(input):
    bricks = dropBricks2(getBricks(input))
    supportedBy = getSupportedBy(bricks)
    bricksAsTuples = []
    for b in bricks:
        # store bricks as tuples of their endponts
        bricksAsTuples.append(b[0]+b[-1])
    fallen = 0
    for brick in bricksAsTuples:
        fallen = fallen + len(removeBricks([brick], supportedBy))
        # print('fallen : ', fallen)
    return fallen       
print('Part 1  : ', solveItPart1(input))
print('Part 2  : ', solveItPart2(input))

   
